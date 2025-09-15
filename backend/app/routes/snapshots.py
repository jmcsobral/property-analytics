from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import io
import pandas as pd

from .. import models, database, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.SnapshotWithCountOut])
def list_snapshots(db: Session = Depends(database.get_db)):
    snaps = db.query(models.Snapshot).order_by(models.Snapshot.upload_date.desc()).all()
    out = []
    for s in snaps:
        cnt = (
            db.query(models.PropertySnapshot)
            .filter(models.PropertySnapshot.snapshot_id == s.id)
            .count()
        )
        out.append(
            schemas.SnapshotWithCountOut(
                id=s.id, upload_date=s.upload_date, properties_count=cnt
            )
        )
    return out


@router.post("/upload", response_model=schemas.SnapshotOut)
async def upload_snapshot(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Please upload an Excel or CSV file.")

    content = await file.read()
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    # Column map based on your sheet names
    map_cols = {
        "date_scraped": "date_scraped",
        "Distrito": "district",
        "Concelho": "city",
        "Zone": "zone",
        "id": "ext_id",
        "href": "url",
        "title": "title",
        "price": "price",
        "price_per_m2": "price_per_m2",
        "area": "area",
        "typology": "typology",
        "floor_info": "floor_info",
        "land_status": "land_status",
        "pricedown_price": "pricedown_price",
        "agency": "agency",
        "parking": "parking",
        "address": "address",
        "description": "description",
        "trespasse": "trespasse",
        "tag": "tags",
        "arrendada": "rented",
        "elevador": "elevator",
        "nova_construcao": "new_construction",
        "image_url": "image_url",
        "video_url": "video_url",
        # "Tipo","Sub-tipo","Sub Tipo" -> ignore for now
    }

    for src, _ in map_cols.items():
        if src not in df.columns:
            # allow missing optional columns silently, but key ones should exist
            pass

    # Create snapshot
    snapshot = models.Snapshot(upload_date=datetime.utcnow())
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    # Normalize booleans
    def to_bool(v):
        if pd.isna(v):
            return None
        s = str(v).strip().lower()
        return s in ["1", "true", "yes", "y", "sim"]

    for _, row in df.iterrows():
        # upsert Property by external id (Excel column 'id')
        ext_id = str(row.get("id", "")).strip()
        if not ext_id:
            # skip rows without id
            continue

        prop = (
            db.query(models.Property)
            .filter(models.Property.property_id == ext_id)
            .first()
        )
        if not prop:
            prop = models.Property(
                property_id=ext_id,
                title=row.get("title"),
                url=row.get("href"),
                area=(float(row["area"]) if not pd.isna(row.get("area")) else None),
                typology=row.get("typology"),
            )
            db.add(prop)
            db.commit()
            db.refresh(prop)
        else:
            # keep latest meta up-to-date too
            prop.title = row.get("title") or prop.title
            prop.url = row.get("href") or prop.url
            if not pd.isna(row.get("area")):
                try:
                    prop.area = float(row.get("area"))
                except Exception:
                    pass
            prop.typology = row.get("typology") or prop.typology
            db.add(prop)
            db.commit()

        ps = models.PropertySnapshot(
            snapshot_id=snapshot.id,
            property_id=prop.id,
            price=(float(row["price"]) if not pd.isna(row.get("price")) else None),
            price_per_m2=(float(row["price_per_m2"]) if not pd.isna(row.get("price_per_m2")) else None),
            district=row.get("Distrito"),
            city=row.get("Concelho"),
            zone=row.get("Zone"),
            typology=row.get("typology"),
            agency=row.get("agency"),
            address=row.get("address"),
            tags=row.get("tag"),
            parking=to_bool(row.get("parking")),
            elevator=to_bool(row.get("elevador")),
            new_construction=to_bool(row.get("nova_construcao")),
            rented=to_bool(row.get("arrendada")),
            trespasse=to_bool(row.get("trespasse")),
            image_url=row.get("image_url"),
            video_url=row.get("video_url"),
            raw_json=None,
        )
        db.add(ps)

    db.commit()
    return snapshot


@router.delete("/{snapshot_id}")
def delete_snapshot(snapshot_id: int, db: Session = Depends(database.get_db)):
    snap = db.query(models.Snapshot).get(snapshot_id)
    if not snap:
        raise HTTPException(status_code=404, detail="Snapshot not found.")
    # delete child snapshots
    db.query(models.PropertySnapshot).filter(models.PropertySnapshot.snapshot_id == snapshot_id).delete()
    db.delete(snap)
    db.commit()
    return {"status": "ok"}
