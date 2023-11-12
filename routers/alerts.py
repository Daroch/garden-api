from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas
import crud

router = APIRouter()


@router.get("/alert_types/", response_model=list[schemas.AlertType])
def read_alert_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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


@router.get("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=schemas.Alert)
def read_alert(
    alert_id: int, db: Session = Depends(get_db)
):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@router.get("/users/{user_id}/plants/{plant_id}/alerts/", response_model=list[schemas.Alert])
def read_alerts_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.alerts_for_plant(
        db, skip=skip, limit=limit, plant_id=plant_id)
    return alerts


@router.post("/users/{user_id}/plants/{plant_id}/alerts", response_model=schemas.Alert, status_code=201)
def create_alert_for_plant(
    plant_id: int, alert_type_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_alert = crud.create_alert_plant(
        db=db, alert=alert, plant_id=plant_id, alert_type_id=alert_type_id)
    return db_alert


@router.patch("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=schemas.Alert)
def update_alert_for_plant(plant_id: int, alert_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)
                           ):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    if plant_id is not db_alert.plant_id:
        raise HTTPException(
            status_code=500, detail="This alert i snot for that plant")
    return crud.update_plant_alert(db=db, plant_id=plant_id, alert=alert)


@router.delete("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=schemas.Alert)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_alert = crud.delete_alert_by_id(db, alert_id=alert_id)
    return db_alert
