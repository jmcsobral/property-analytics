from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ------------------------
# Annotations
# ------------------------
class AnnotationBase(BaseModel):
    reviewed: Optional[bool] = None
    contacted: Optional[bool] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class AnnotationCreate(AnnotationBase):
    property_id: int


class AnnotationOut(AnnotationBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# ------------------------
# Properties
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
# PropertySnapshots
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
# Snapshots
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


class SnapshotWithCountOut(SnapshotOut):
    properties_count: int


# ------------------------
# Combined property
# ------------------------
class PropertyFullOut(PropertyOut):
    snapshots: List[PropertySnapshotOut] = []
    annotations: List[AnnotationOut] = []

    class Config:
        from_attributes = True


# ------------------------
# Analytics payloads
# ------------------------
class AvgPricePerM2Out(BaseModel):
    month: str
    avg_price: float


class PriceDistributionOut(BaseModel):
    month: str
    min_price: Optional[float]
    median_price: Optional[float]
    max_price: Optional[float]


class ListingsPerMonthOut(BaseModel):
    month: str
    listings: int


# ------------------------
# Options payload
# ------------------------
class PropertiesOptionsOut(BaseModel):
    districts: List[str]
    cities: List[str]
    zones: List[str]
    typologies: List[str]
    agencies: List[str]
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ------------------------
# Annotations
# ------------------------
class AnnotationBase(BaseModel):
    reviewed: Optional[bool] = None
    contacted: Optional[bool] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class AnnotationCreate(AnnotationBase):
    property_id: int


class AnnotationOut(AnnotationBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# ------------------------
# Properties
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
# PropertySnapshots
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
# Snapshots
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


class SnapshotWithCountOut(SnapshotOut):
    properties_count: int


# ------------------------
# Combined property
# ------------------------
class PropertyFullOut(PropertyOut):
    snapshots: List[PropertySnapshotOut] = []
    annotations: List[AnnotationOut] = []

    class Config:
        from_attributes = True


# ------------------------
# Analytics payloads
# ------------------------
class AvgPricePerM2Out(BaseModel):
    month: str
    avg_price: float


class PriceDistributionOut(BaseModel):
    month: str
    min_price: Optional[float]
    median_price: Optional[float]
    max_price: Optional[float]


class ListingsPerMonthOut(BaseModel):
    month: str
    listings: int


# ------------------------
# Options payload
# ------------------------
class PropertiesOptionsOut(BaseModel):
    districts: List[str]
    cities: List[str]
    zones: List[str]
    typologies: List[str]
    agencies: List[str]
