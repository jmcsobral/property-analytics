from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ------------------------
# Annotation Schemas
# ------------------------
class AnnotationBase(BaseModel):
    reviewed: Optional[bool] = None
    contacted: Optional[bool] = None
    notes: Optional[str] = None
    # NEW: interesting flag ("Yes" / "No" / None)
    interesting: Optional[str] = None

    class Config:
        from_attributes = True


class AnnotationCreate(AnnotationBase):
    # property_id is used server-side from the path param, but keep for compatibility
    property_id: Optional[int] = None


class AnnotationOut(AnnotationBase):
    id: int
    property_id: int

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
    status: Optional[str] = None
    raw_json: Optional[str] = None

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
    property_id: int
    snapshot_id: int

    class Config:
        from_attributes = True


# ------------------------
# Snapshot Schemas
# ------------------------
class SnapshotBase(BaseModel):
    id: int
    upload_date: datetime

    class Config:
        from_attributes = True


class SnapshotCreate(BaseModel):
    pass


class SnapshotOut(SnapshotBase):
    class Config:
        from_attributes = True


# ------------------------
# Combined Property + Snapshot + Annotation
# ------------------------
class PropertyFullOut(PropertyOut):
    snapshots: List[PropertySnapshotOut] = []
    annotations: List[AnnotationOut] = []

    class Config:
        from_attributes = True


# ------------------------
# Analytics Out Schemas
# ------------------------
class AvgPricePerM2Out(BaseModel):
    month: str
    avg_price: float


class PriceDistributionOut(BaseModel):
    month: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    median_price: Optional[float] = None


class ListingsPerMonthOut(BaseModel):
    month: str
    count: int

class PropertiesOptionsOut(BaseModel):
    districts: List[str]
    cities: List[str]
    zones: List[str]
    typologies: List[str]
    agencies: List[str]