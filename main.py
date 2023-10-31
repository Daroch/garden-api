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