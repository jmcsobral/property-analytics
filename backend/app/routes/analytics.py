from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from .. import models, database, schemas
from .properties import apply_filters

router = APIRouter()


@router.get("/avg_price_per_m2", response_model=List[schemas.AvgPricePerM2Out])
def avg_price_per_m2(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_ppm2: Optional[float] = Query(None),
    max_ppm2: Optional[float] = Query(None),
):
    month_expr = func.date_trunc("month", models.Snapshot.upload_date).label("month")

    query = (
        db.query(
            month_expr,
            func.avg(models.PropertySnapshot.price_per_m2).label("avg_price"),
        )
        .join(models.PropertySnapshot.snapshot)
    )

    filters = {
        "district": district, "city": city, "zone": zone,
        "typology": typology, "agency": agency,
        "min_price": min_price, "max_price": max_price,
        "min_ppm2": min_ppm2, "max_ppm2": max_ppm2,
    }
    query = apply_filters(query, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()
    return [
        {"month": r.month.strftime("%Y-%m"), "avg_price": float(r.avg_price)}
        for r in results if r.avg_price is not None
    ]


@router.get("/price_distribution", response_model=List[schemas.PriceDistributionOut])
def price_distribution(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_ppm2: Optional[float] = Query(None),
    max_ppm2: Optional[float] = Query(None),
):
    month_expr = func.date_trunc("month", models.Snapshot.upload_date).label("month")

    query = (
        db.query(
            month_expr,
            func.min(models.PropertySnapshot.price_per_m2).label("min"),
            func.max(models.PropertySnapshot.price_per_m2).label("max"),
            func.percentile_cont(0.5).within_group(models.PropertySnapshot.price_per_m2).label("median"),
        )
        .join(models.PropertySnapshot.snapshot)
    )

    filters = {
        "district": district, "city": city, "zone": zone,
        "typology": typology, "agency": agency,
        "min_price": min_price, "max_price": max_price,
        "min_ppm2": min_ppm2, "max_ppm2": max_ppm2,
    }
    query = apply_filters(query, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()
    return [
        {
            "month": r.month.strftime("%Y-%m"),
            "min": float(r.min) if r.min is not None else None,
            "median": float(r.median) if r.median is not None else None,
            "max": float(r.max) if r.max is not None else None,
        }
        for r in results
    ]


@router.get("/listings_per_month", response_model=List[schemas.ListingsPerMonthOut])
def listings_per_month(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_ppm2: Optional[float] = Query(None),
    max_ppm2: Optional[float] = Query(None),
):
    month_expr = func.date_trunc("month", models.Snapshot.upload_date).label("month")

    query = (
        db.query(
            month_expr,
            func.count(models.PropertySnapshot.id).label("count"),
        )
        .join(models.PropertySnapshot.snapshot)
    )

    filters = {
        "district": district, "city": city, "zone": zone,
        "typology": typology, "agency": agency,
        "min_price": min_price, "max_price": max_price,
        "min_ppm2": min_ppm2, "max_ppm2": max_ppm2,
    }
    query = apply_filters(query, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()
    return [{"month": r.month.strftime("%Y-%m"), "count": int(r.count)} for r in results]
