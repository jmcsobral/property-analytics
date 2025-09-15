# backend/app/routes/analytics.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from .. import models, database
from .properties import apply_filters

router = APIRouter()


# ------------------------
# Average price per m² per month
# ------------------------
@router.get("/avg_price_per_m2")
def avg_price(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
):
    month_expr = func.date_trunc("month", models.Snapshot.upload_date).label("month")

    query = (
        db.query(
            month_expr,
            func.avg(models.PropertySnapshot.price_per_m2).label("avg_price")
        )
        .join(models.PropertySnapshot.snapshot)
    )

    filters = {
        "district": district,
        "city": city,
        "zone": zone,
        "typology": typology,
        "agency": agency,
    }
    query = apply_filters(query, db, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()

    return [
        {"month": r.month.strftime("%Y-%m"), "avg_price": float(r.avg_price)}
        for r in results if r.avg_price is not None
    ]


# ------------------------
# Price distribution per month (min, max, median)
# ------------------------
@router.get("/price_distribution")
def price_distribution(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
):
    month_expr = func.date_trunc("month", models.Snapshot.upload_date).label("month")

    query = (
        db.query(
            month_expr,
            func.min(models.PropertySnapshot.price_per_m2).label("min_price"),
            func.max(models.PropertySnapshot.price_per_m2).label("max_price"),
            func.percentile_cont(0.5).within_group(models.PropertySnapshot.price_per_m2).label("median_price"),
        )
        .join(models.PropertySnapshot.snapshot)
    )

    filters = {
        "district": district,
        "city": city,
        "zone": zone,
        "typology": typology,
        "agency": agency,
    }
    query = apply_filters(query, db, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()

    return [
        {
            "month": r.month.strftime("%Y-%m"),
            "min_price": float(r.min_price) if r.min_price is not None else None,
            "max_price": float(r.max_price) if r.max_price is not None else None,
            "median_price": float(r.median_price) if r.median_price is not None else None,
        }
        for r in results
    ]


# ------------------------
# Listings count per month
# ------------------------
@router.get("/listings_per_month")
def listings_per_month(
    db: Session = Depends(database.get_db),
    district: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    zone: Optional[str] = Query(None),
    typology: Optional[str] = Query(None),
    agency: Optional[str] = Query(None),
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
        "district": district,
        "city": city,
        "zone": zone,
        "typology": typology,
        "agency": agency,
    }
    query = apply_filters(query, db, filters)

    results = query.group_by(month_expr).order_by(month_expr).all()

    return [
        {"month": r.month.strftime("%Y-%m"), "count": int(r.count)}
        for r in results
    ]
