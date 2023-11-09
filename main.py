from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get('/')
def root():
    return {"msg": "Hello, I am FastAPI"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/plants/", response_model=schemas.Plant)
def create_plant_for_user(
    user_id: int, category_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_plant(db=db, plant=plant, user_id=user_id, category_id=category_id)


@app.get("/users/{user_id}/plants", response_model=list[schemas.Plant])
def read_plants_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plants = crud.get_plants_for_user(db, skip=skip, limit=limit, user_id=user_id)
    return plants


@app.get("/users/{user_id}/plants/{plant_id}", response_model=schemas.Plant)
def read_plant(
    plant_id: int, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if  db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db_plant


@app.patch("/users/{user_id}/plants/{plant_id}", response_model=schemas.Plant)
def update_plant_for_user(user_id: int, plant_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if  db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if  user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.update_user_plant(db=db, plant_id=plant_id, plant=plant)



@app.get("/categories/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="category already exists")
    return crud.create_category(db=db, category=category)


@app.get("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=schemas.Journal)
def read_journal(
    journal_id: int, db: Session = Depends(get_db)
):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if  db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    return db_journal

@app.get("/users/{user_id}/plants/{plant_id}/journals/", response_model=list[schemas.Journal])
def read_journals_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.journals_for_plant(db, skip=skip, limit=limit, plant_id=plant_id)
    return journals

@app.post("/users/{user_id}/plants/{plant_id}/journals", response_model=schemas.Journal)
def create_journal_for_plant(
    plant_id: int, journal: schemas.JournalCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_journal = crud.create_journal_plant(db=db, journal=journal, plant_id=plant_id)
    return db_journal

@app.patch("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=schemas.Journal)
def update_journal_for_plant(plant_id: int, journal_id: int, journal: schemas.JournalCreate, db: Session = Depends(get_db)
):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if  db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    if  plant_id is not db_journal.plant_id:
        raise HTTPException(status_code=500, detail="This journal i snot for that plant")
    return crud.update_plant_journal(db=db, plant_id=plant_id, plant=plant)


@app.get("/alert_types/", response_model=list[schemas.AlertType])
def read_alert_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alert_types = crud.get_alert_types(db, skip=skip, limit=limit)
    return alert_types

@app.post("/alert_types/", response_model=schemas.AlertType)
def create_alert_type(alert_type: schemas.AlertTypeCreate, db: Session = Depends(get_db)):
    db_alert_type = crud.get_alert_type_by_name(db, alert_name=alert_type.alert_name)
    if db_alert_type:
        raise HTTPException(status_code=400, detail="Alert type already exists")
    return crud.create_alert_type(db=db, alert_type=alert_type)


@app.get("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=schemas.Alert)
def read_alert(
    alert_id: int, db: Session = Depends(get_db)
):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if  db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert

@app.get("/users/{user_id}/plants/{plant_id}/alerts/", response_model=list[schemas.Alert])
def read_alerts_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.alerts_for_plant(db, skip=skip, limit=limit, plant_id=plant_id)
    return alerts

@app.post("/users/{user_id}/plants/{plant_id}/alerts", response_model=schemas.Alert)
def create_alert_for_plant(
    plant_id: int, alert_type_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_alert = crud.create_alert_plant(db=db, alert=alert, plant_id=plant_id, alert_type_id=alert_type_id)
    return db_alert

@app.patch("/users/{user_id}/plants/{plant_id}/alerts/{alert_id}", response_model=schemas.Alert)
def update_alert_for_plant(plant_id: int, alert_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)
):
    db_alert = crud.get_alert(db, alert_id=alert_id)
    if  db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    if  plant_id is not db_alert.plant_id:
        raise HTTPException(status_code=500, detail="This alert i snot for that plant")
    return crud.update_plant_alert(db=db, plant_id=plant_id, alert=alert)