# backend/app/routes/properties.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from .. import models, schemas, database

router = APIRouter()


# ------------------------
# Shared filter function
# ------------------------
def apply_filters(query, filters: dict):
    """Reusable filters across properties, snapshots, and analytics."""
    if filters.get("district"):
        query = query.filter(models.PropertySnapshot.district == filters["district"])
    if filters.get("city"):
        query = query.filter(models.PropertySnapshot.city == filters["city"])
    if filters.get("zone"):
        query = query.filter(models.PropertySnapshot.zone == filters["zone"])
    if filters.get("typology"):
        query = query.filter(models.PropertySnapshot.typology == filters["typology"])
    if filters.get("agency"):
        query = query.filter(models.PropertySnapshot.agency == filters["agency"])
    if filters.get("parking") is not None:
        query = query.filter(models.PropertySnapshot.parking == filters["parking"])
    if filters.get("elevator") is not None:
        query = query.filter(models.PropertySnapshot.elevator == filters["elevator"])
    if filters.get("new_construction") is not None:
        query = query.filter(models.PropertySnapshot.new_construction == filters["new_construction"])
    if filters.get("rented") is not None:
        query = query.filter(models.PropertySnapshot.rented == filters["rented"])
    if filters.get("trespasse") is not None:
        query = query.filter(models.PropertySnapshot.trespasse == filters["trespasse"])
    return query


# ------------------------
# List all properties
# ------------------------
@router.get("/", response_model=list[schemas.PropertyFullOut])
def list_properties(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
    parking: Optional[bool] = Query(None),
    elevator: Optional[bool] = Query(None),
    new_construction: Optional[bool] = Query(None),
    rented: Optional[bool] = Query(None),
    trespasse: Optional[bool] = Query(None),
):
    """
    Returns a list of properties with their latest snapshot and annotations.
    """

    # Base query: join properties with snapshots + eager load relationships
    query = (
        db.query(models.Property)
        .options(
            joinedload(models.Property.snapshots),
            joinedload(models.Property.annotations),
        )
        .join(models.Property.snapshots)
        .join(models.Snapshot)
    )

    filters = {
        "district": district,
        "city": city,
        "zone": zone,
        "typology": typology,
        "agency": agency,
        "parking": parking,
        "elevator": elevator,
        "new_construction": new_construction,
        "rented": rented,
        "trespasse": trespasse,
    }
    query = apply_filters(query, filters)

    return query.all()
