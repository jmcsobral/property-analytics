# backend/app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ------------------------
# Snapshot Schemas
# ------------------------
class SnapshotBase(BaseModel):
    id: int
    upload_date: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


class SnapshotCreate(BaseModel):
    """Used for uploading new snapshots (Excel files)."""
    pass


class SnapshotOut(SnapshotBase):
    class Config:
        from_attributes = True


# ------------------------
# Property Schemas
# ------------------------
class PropertyBase(BaseModel):
    property_id: str
    title: Optional[str] = None
    url: Optional[str] = None
    area: Optional[float] = None
    typology: Optional[str] = None

    class Config:
        from_attributes = True


class PropertyOut(PropertyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------------
# Property Snapshot Schemas
# ------------------------
class PropertySnapshotBase(BaseModel):
    price: Optional[float] = None
    price_per_m2: Optional[float] = None
    district: Optional[str] = None
    city: Optional[str] = None
    zone: Optional[str] = None
    typology: Optional[str] = None
    agency: Optional[str] = None
    address: Optional[str] = None
    tags: Optional[str] = None
    parking: Optional[bool] = None
    elevator: Optional[bool] = None
    new_construction: Optional[bool] = None
    rented: Optional[bool] = None
    trespasse: Optional[bool] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

    class Config:
        from_attributes = True


class PropertySnapshotOut(PropertySnapshotBase):
    id: int
    snapshot_id: int
    property_id: int

    class Config:
        from_attributes = True


# ------------------------
# Annotation Schemas
# ------------------------
class AnnotationBase(BaseModel):
    reviewed: Optional[bool] = None
    contacted: Optional[bool] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationOut(AnnotationBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# ------------------------
# Combined Property + Snapshot + Annotation
# ------------------------
class PropertyFullOut(PropertyOut):
    snapshots: list[PropertySnapshotOut] = []
    annotations: list[AnnotationOut] = []

    # Optional: expose the latest snapshot/annotation directly
    latest_snapshot: Optional[PropertySnapshotOut] = None
    latest_annotation: Optional[AnnotationOut] = None

    class Config:
        from_attributes = True
