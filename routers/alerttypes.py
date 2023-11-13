from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas
import crud

router = APIRouter(tags=["Alert Types"])


@router.get("/alert_types/", response_model=list[schemas.AlertType])
def get_all_alert_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alert_types = crud.get_alert_types(db, skip=skip, limit=limit)
    return alert_types


@router.post("/alert_types/", response_model=schemas.AlertType, status_code=201)
def create_alert_type(alert_type: schemas.AlertTypeCreate, db: Session = Depends(get_db)):
    db_alert_type = crud.get_alert_type_by_name(
        db, alert_name=alert_type.alert_name)
    if db_alert_type:
        raise HTTPException(
            status_code=400, detail="Alert type already exists")
    return crud.create_alert_type(db=db, alert_type=alert_type)
