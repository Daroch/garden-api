from typing import Annotated
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import AlertType, User, AlertTypeCreate
import crud
import auth

router = APIRouter(tags=["Alert Types"])


@router.get("/alert_types", response_model=list[AlertType])
def get_all_alert_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alert_types = crud.get_alert_types(db, skip=skip, limit=limit)
    return alert_types


@router.post("/addalert_type", response_model=AlertType, status_code=201)
def create_alert_type(current_user: Annotated[User, Security(
        auth.get_current_active_user)], alert_type: AlertTypeCreate, db: Session = Depends(get_db)):
    db_alert_type = crud.get_alert_type_by_name(
        db, alert_name=alert_type.alert_name)
    if db_alert_type:
        raise HTTPException(
            status_code=400, detail="Alert type already exists")
    if current_user.name != "admin":
        raise HTTPException(
            status_code=403, detail="Only admin can create alert types")
    return crud.create_alert_type(db=db, alert_type=alert_type)
