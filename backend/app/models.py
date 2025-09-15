from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    area = Column(Float, nullable=True)
    typology = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    snapshots = relationship(
        "PropertySnapshot", back_populates="property", cascade="all, delete-orphan"
    )
    annotations = relationship(
        "Annotation", back_populates="property", cascade="all, delete-orphan"
    )

class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    upload_date = Column(DateTime, server_default=func.now())

    snapshots = relationship(
        "PropertySnapshot", back_populates="snapshot", cascade="all, delete-orphan"
    )

class PropertySnapshot(Base):
    __tablename__ = "property_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id", ondelete="CASCADE"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)

    price = Column(Float, nullable=True)
    price_per_m2 = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    raw_json = Column(Text, nullable=True)

    district = Column(String, index=True, nullable=True)
    city = Column(String, index=True, nullable=True)
    zone = Column(String, index=True, nullable=True)
    typology = Column(String, index=True, nullable=True)
    agency = Column(String, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)
    tags = Column(String, index=True, nullable=True)

    parking = Column(Boolean, server_default="false")
    elevator = Column(Boolean, server_default="false")
    new_construction = Column(Boolean, server_default="false")
    rented = Column(Boolean, server_default="false")
    trespasse = Column(Boolean, server_default="false")

    image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)

    property = relationship("Property", back_populates="snapshots")
    snapshot = relationship("Snapshot", back_populates="snapshots")

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    reviewed = Column(Boolean, default=False)
    contacted = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    property = relationship("Property", back_populates="annotations")
