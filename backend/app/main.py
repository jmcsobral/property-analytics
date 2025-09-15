from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import properties, snapshots, annotations, analytics
from .database import engine, Base, SessionLocal
from . import models
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Analytics")

# CORS setup
origins = [
    "http://localhost:3000",   # local dev
    "http://frontend:3000"     # docker container
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(snapshots.router, prefix="/snapshots", tags=["Snapshots"])
app.include_router(annotations.router, prefix="/annotations", tags=["Annotations"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

# ---- Auto-seed fake data ----
from sqlalchemy.orm import Session
def seed_data():
    db: Session = SessionLocal()
    if db.query(models.Snapshot).count() == 0:
        snap = models.Snapshot(upload_date=datetime.utcnow())
        db.add(snap)
        db.commit()
        db.refresh(snap)

        fake_props = [
            {
                "property_id": f"FAKE{i}",
                "title": f"Shop {i} in Porto",
                "url": "https://www.idealista.pt/en/",
                "area": 100 + i*10,
                "typology": "Loja",
                "price": 100000 + i*5000,
                "price_per_m2": 1000 + i*50,
                "image_url": "https://via.placeholder.com/150"
            }
            for i in range(1, 6)
        ]

        for p in fake_props:
            prop = models.Property(
                property_id=p["property_id"],
                title=p["title"],
                url=p["url"],
                area=p["area"],
                typology=p["typology"],
            )
            db.add(prop)
            db.commit()
            db.refresh(prop)

            snap_data = models.PropertySnapshot(
                snapshot_id=snap.id,
                property_id=prop.id,
                price=p["price"],
                price_per_m2=p["price_per_m2"],
                raw_json=str(p)
            )
            db.add(snap_data)

        db.commit()
    db.close()

seed_data()
