from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, database

router = APIRouter()


@router.get("/{property_id}", response_model=list[schemas.AnnotationOut])
def list_annotations(property_id: int, db: Session = Depends(database.get_db)):
    return (
        db.query(models.Annotation)
        .filter(models.Annotation.property_id == property_id)
        .all()
    )


@router.post("/{property_id}", response_model=schemas.AnnotationOut)
def create_or_update_annotation(
    property_id: int,
    payload: schemas.AnnotationCreate,
    db: Session = Depends(database.get_db),
):
    # Ensure property exists
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    # Upsert single annotation row per property (keeps UI simple)
    ann = (
        db.query(models.Annotation)
        .filter(models.Annotation.property_id == property_id)
        .first()
    )
    if ann:
        # Update existing
        if payload.reviewed is not None:
            ann.reviewed = payload.reviewed
        if payload.contacted is not None:
            ann.contacted = payload.contacted
        if payload.notes is not None:
            ann.notes = payload.notes
        if payload.interesting is not None:
            # Only allow "Yes" or "No" (or None)
            if payload.interesting not in (None, "Yes", "No"):
                raise HTTPException(status_code=400, detail="interesting must be 'Yes' or 'No'")
            ann.interesting = payload.interesting
    else:
        # Create new
        ann = models.Annotation(
            property_id=property_id,
            reviewed=payload.reviewed or False,
            contacted=payload.contacted or False,
            notes=payload.notes,
            interesting=payload.interesting if payload.interesting in (None, "Yes", "No") else None,
        )
        db.add(ann)

    db.commit()
    db.refresh(ann)
    return ann
