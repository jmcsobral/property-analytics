from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from .. import models, schemas, database

router = APIRouter()


def apply_filters(query, filters: dict):
    # categorical filters
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

    # boolean flags
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

    # numeric ranges — price & price_per_m2
    if filters.get("min_price") is not None:
        query = query.filter(models.PropertySnapshot.price >= filters["min_price"])
    if filters.get("max_price") is not None:
        query = query.filter(models.PropertySnapshot.price <= filters["max_price"])
    if filters.get("min_ppm2") is not None:
        query = query.filter(models.PropertySnapshot.price_per_m2 >= filters["min_ppm2"])
    if filters.get("max_ppm2") is not None:
        query = query.filter(models.PropertySnapshot.price_per_m2 <= filters["max_ppm2"])

    return query


@router.get("/", response_model=List[schemas.PropertyFullOut])
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
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_ppm2: Optional[float] = Query(None),
    max_ppm2: Optional[float] = Query(None),
):
    query = (
        db.query(models.Property)
        .options(
            joinedload(models.Property.snapshots),
            joinedload(models.Property.annotations),
        )
        # ensure we have at least one snapshot row to filter on
        .join(models.Property.snapshots)
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
        "min_price": min_price,
        "max_price": max_price,
        "min_ppm2": min_ppm2,
        "max_ppm2": max_ppm2,
    }
    query = apply_filters(query, filters)
    return query.all()