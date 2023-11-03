from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import engine, localSession
from schemas import PlantData, PlantId
from models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
  db = localSession()
  try:
    yield db
  finally:
    db.close()
    
@app.get('/')
def root():
    return 'Hello, I am FastAPI'

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


@app.get('/api/plants', response_model=list[PlantId])
def get_plants(db: Session = Depends(get_db)):
  return crud.get_plants(db)
  
@app.get('/api/plants/{id}')
def get_plant_by_id(id, db: Session = Depends(get_db)):
  plant_by_id = crud.get_plant_by_id(db=db, id=id)
  if (plant_by_id and plant_by_id!={}):
    return plant_by_id
  else:
    raise HTTPException(status_code=404, detail='Plant not found')