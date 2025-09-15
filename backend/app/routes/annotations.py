from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter()


# ---- Create annotation ----
@router.post("/{property_id}", response_model=schemas.AnnotationOut)
def create_annotation(property_id: int, annotation: schemas.AnnotationCreate, db: Session = Depends(database.get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    note = models.Annotation(property_id=property_id, note=annotation.note)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# ---- List annotations for property ----
@router.get("/{property_id}", response_model=List[schemas.AnnotationOut])
def list_annotations(property_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Annotation).filter(models.Annotation.property_id == property_id).all()
