from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List

from .. import models, schemas, database

router = APIRouter()


def apply_filters(query, filters: dict):
    """
    Reusable filters for both property listing and analytics queries.
    Works with a query that already involves PropertySnapshot (and Property for area).
    """

    # Categorical equals
    if filters.get("district"):
        query = query.filter(models.PropertySnapshot.district == filters["district"])
    if filters.get("city"):
        query = query.filter(models.PropertySnapshot.city == filters["city"])
    if filters.get("zone"):
        query = query.filter(models.PropertySnapshot.zone == filters["zone"])
    if filters.get("agency"):
        query = query.filter(models.PropertySnapshot.agency == filters["agency"])

    # Typology can be list (e.g., ["T2","T3","T4"])
    typs = filters.get("typology_list")
    if typs:
        query = query.filter(models.PropertySnapshot.typology.in_(typs))
    elif filters.get("typology"):
        query = query.filter(models.PropertySnapshot.typology == filters["typology"])

    # Boolean flags
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

    # Text search (ILIKE)
    if filters.get("search_address"):
        query = query.filter(models.PropertySnapshot.address.ilike(f"%{filters['search_address']}%"))
    if filters.get("search_tags"):
        query = query.filter(models.PropertySnapshot.tags.ilike(f"%{filters['search_tags']}%"))

    # Numeric ranges
    if filters.get("min_price") is not None:
        query = query.filter(models.PropertySnapshot.price >= filters["min_price"])
    if filters.get("max_price") is not None:
        query = query.filter(models.PropertySnapshot.price <= filters["max_price"])

    if filters.get("min_price_per_m2") is not None:
        query = query.filter(models.PropertySnapshot.price_per_m2 >= filters["min_price_per_m2"])
    if filters.get("max_price_per_m2") is not None:
        query = query.filter(models.PropertySnapshot.price_per_m2 <= filters["max_price_per_m2"])

    # area is on Property (not on PropertySnapshot)
    if filters.get("min_area") is not None:
        query = query.filter(models.Property.area >= filters["min_area"])
    if filters.get("max_area") is not None:
        query = query.filter(models.Property.area <= filters["max_area"])

    return query


@router.get("/", response_model=List[schemas.PropertyFullOut])
def list_properties(
    db: Session = Depends(database.get_db),
    # categoricals
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
    # typology: can be repeated (typology=T2&typology=T3)
    typology: Optional[List[str]] = Query(None),
    # booleans
    parking: Optional[bool] = Query(None),
    elevator: Optional[bool] = Query(None),
    new_construction: Optional[bool] = Query(None),
    rented: Optional[bool] = Query(None),
    trespasse: Optional[bool] = Query(None),
    # ranges
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_price_per_m2: Optional[float] = Query(None),
    max_price_per_m2: Optional[float] = Query(None),
    min_area: Optional[float] = Query(None),
    max_area: Optional[float] = Query(None),
    # search
    search_address: Optional[str] = Query(None),
    search_tags: Optional[str] = Query(None),
):
    query = (
        db.query(models.Property)
        .join(models.Property.snapshots)   # ensure PropertySnapshot is in the query
        .options(
            joinedload(models.Property.snapshots),
            joinedload(models.Property.annotations),
        )
    )

    filters = {
        "district": district,
        "city": city,
        "zone": zone,
        "agency": agency,
        "typology_list": typology,
        "parking": parking,
        "elevator": elevator,
        "new_construction": new_construction,
        "rented": rented,
        "trespasse": trespasse,
        "min_price": min_price,
        "max_price": max_price,
        "min_price_per_m2": min_price_per_m2,
        "max_price_per_m2": max_price_per_m2,
        "min_area": min_area,
        "max_area": max_area,
        "search_address": search_address,
        "search_tags": search_tags,
    }

    query = apply_filters(query, filters)
    return query.all()


@router.get("/options", response_model=schemas.PropertiesOptionsOut)
def options(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
):
    """
    Returns dependent dropdown options:
    - districts (always full set)
    - cities (optionally filtered by district)
    - zones (optionally filtered by district and/or city)
    - typologies (T* sorted numerically first)
    - agencies
    """
    base = db.query(models.PropertySnapshot)

    # districts (full)
    districts = (
        db.query(models.PropertySnapshot.district)
        .filter(models.PropertySnapshot.district.isnot(None))
        .distinct()
        .order_by(models.PropertySnapshot.district.asc())
        .all()
    )
    districts = [d[0] for d in districts]

    # cities (filtered by district)
    cities_q = base
    if district:
        cities_q = cities_q.filter(models.PropertySnapshot.district == district)
    cities = (
        cities_q.with_entities(models.PropertySnapshot.city)
        .filter(models.PropertySnapshot.city.isnot(None))
        .distinct()
        .order_by(models.PropertySnapshot.city.asc())
        .all()
    )
    cities = [c[0] for c in cities]

    # zones (filtered by district and/or city)
    zones_q = base
    if district:
        zones_q = zones_q.filter(models.PropertySnapshot.district == district)
    if city:
        zones_q = zones_q.filter(models.PropertySnapshot.city == city)
    zones = (
        zones_q.with_entities(models.PropertySnapshot.zone)
        .filter(models.PropertySnapshot.zone.isnot(None))
        .distinct()
        .order_by(models.PropertySnapshot.zone.asc())
        .all()
    )
    zones = [z[0] for z in zones]

    # typologies: sort T* numerically first, then others
    raw_typs = (
        db.query(models.PropertySnapshot.typology)
        .filter(models.PropertySnapshot.typology.isnot(None))
        .distinct()
        .all()
    )
    raw_typs = [t[0] for t in raw_typs]
    t_like = [t for t in raw_typs if t and t.upper().startswith("T")]
    not_t = [t for t in raw_typs if not (t and t.upper().startswith("T"))]

    def t_key(t):
        # Extract the number after T; fallback large to push unknown last
        try:
            return int("".join(ch for ch in t.upper()[1:] if ch.isdigit()))
        except Exception:
            return 999

    typologies = sorted(t_like, key=t_key) + sorted(not_t)

    # agencies
    agencies = (
        db.query(models.PropertySnapshot.agency)
        .filter(models.PropertySnapshot.agency.isnot(None))
        .distinct()
        .order_by(models.PropertySnapshot.agency.asc())
        .all()
    )
    agencies = [a[0] for a in agencies]

    return schemas.PropertiesOptionsOut(
        districts=districts,
        cities=cities,
        zones=zones,
        typologies=typologies,
        agencies=agencies,
    )
