# backend/app/routes/snapshots.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
from .. import models, database, schemas

router = APIRouter()


# ------------------------
# List all snapshots
# ------------------------
@router.get("/", response_model=list[schemas.SnapshotOut])
def list_snapshots(db: Session = Depends(database.get_db)):
    """
    Return all uploaded snapshots with basic metadata.
    """
    return db.query(models.Snapshot).all()


# ------------------------
# Upload new snapshot
# ------------------------
@router.post("/upload", response_model=schemas.SnapshotOut)
async def upload_snapshot(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Upload an Excel file.")

    content = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Excel: {e}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Excel file is empty.")

    # Map Excel column names -> backend fields
    column_mapping = {
        "Distrito": "district",
        "Concelho": "city",
        "Zone": "zone",
        "id": "property_id",
        "href": "url",
        "title": "title",
        "price": "price",
        "price_per_m2": "price_per_m2",
        "area": "area",
        "typology": "typology",
        "agency": "agency",
        "parking": "parking",
        "address": "address",
        "tag": "tags",
        "arrendada": "rented",
        "elevador": "elevator",
        "nova_construcao": "new_construction",
        "trespasse": "trespasse",
        "image_url": "image_url",
        "video_url": "video_url",
    }

    df = df.rename(columns=column_mapping)

    # Create snapshot record
    snapshot = models.Snapshot()
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    for _, row in df.iterrows():
        # Ensure property exists
        prop = db.query(models.Property).filter_by(property_id=str(row.get("property_id"))).first()
        if not prop:
            prop = models.Property(
                property_id=str(row.get("property_id")),
                title=row.get("title", "Untitled"),
                url=row.get("url", None),
                area=row.get("area", None),
                typology=row.get("typology", None),
            )
            db.add(prop)
            db.commit()
            db.refresh(prop)

        # Add snapshot row
        snap_data = models.PropertySnapshot(
            snapshot_id=snapshot.id,
            property_id=prop.id,
            price=row.get("price"),
            price_per_m2=row.get("price_per_m2"),
            district=row.get("district"),
            city=row.get("city"),
            zone=row.get("zone"),
            typology=row.get("typology"),
            agency=row.get("agency"),
            address=row.get("address"),
            tags=row.get("tags"),
            parking=bool(row.get("parking", False)),
            elevator=bool(row.get("elevator", False)),
            new_construction=bool(row.get("new_construction", False)),
            rented=bool(row.get("rented", False)),
            trespasse=bool(row.get("trespasse", False)),
            raw_json=row.to_json(),
        )
        db.add(snap_data)

    db.commit()
    return snapshot


# ------------------------
# Delete a snapshot
# ------------------------
@router.delete("/{snapshot_id}")
def delete_snapshot(snapshot_id: int, db: Session = Depends(database.get_db)):
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Cascade delete snapshots
    db.query(models.PropertySnapshot).filter(models.PropertySnapshot.snapshot_id == snapshot_id).delete()
    db.delete(snapshot)
    db.commit()
    return {"message": f"Snapshot {snapshot_id} deleted"}
