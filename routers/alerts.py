from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import Alert, AlertCreate
import crud
from alerts_system import send_alerts

router = APIRouter(tags=["Alerts"])


@router.get("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=Alert)
def get_alert_details(
    alert_id: int, db: Session = Depends(get_db)
):
    db_alert = crud.get_alert_details(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@router.get("/users/{user_id}/plants/{plant_id}/alerts", response_model=list[Alert])
def get_alerts_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.get_alerts_for_plant(
        db, skip=skip, limit=limit, plant_id=plant_id)
    return alerts


@router.get("/users/{user_id}/alerts", response_model=list[Alert])
def get_alerts_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.get_alerts_for_user(
        db, skip=skip, limit=limit, user_id=user_id)
    return alerts


@router.post("/users/{user_id}/plants/{plant_id}/addalert", response_model=Alert, status_code=201)
def create_alert_for_plant(
    plant_id: int, alert: AlertCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_alert = crud.create_alert_plant(
        db=db, alert=alert, plant_id=plant_id)
    return db_alert


@router.patch("/users/{user_id}/plants/{plant_id}/updatealert/{alert_id}", response_model=Alert)
def update_alert(user_id: int, plant_id: int, alert_id: int, alert: AlertCreate, db: Session = Depends(get_db)
                 ):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_alert.plant_id = plant_id
    return crud.update_alert_plant(db=db, alert_id=alert_id, alert=alert)


@router.delete("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=Alert)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db_alert = crud.delete_alert_by_id(db, alert_id=alert_id)
    return db_alert


@router.get("/all_alerts")
def get_all_alerts(db: Session = Depends(get_db)):
    alerts = crud.get_all_alerts(db)
    return alerts


@router.get("/alerts_to_email")
def get_alerts_to_send_email(db: Session = Depends(get_db)):
    alerts = crud.get_alerts_to_send_email(db)
    return alerts


@router.get("/send_alerts_to_email")
def send_alerts_to_email(db: Session = Depends(get_db)):
    send_alerts(db)
