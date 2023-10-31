from sqlalchemy.orm import Session

from models import Plant
from schemas import PlantData

def get_plants(db: Session):
   return db.query(Plant).all()
 
def get_plant_by_id(db: Session, id: int):
  return db.query(Plant).filter(Plant.id == id)

def get_plant_by_name(db: Session, name: str):
  return db.query(Plant).filter(Plant.name == name)

def create_plant(db: Session, plant: PlantData):
  new_plant = Plant(name=plant.name, description=plant.description, publish=plant.publish)
  db.add(new_plant)
  db.commit()
  db.flush(new_plant)
  return new_plant