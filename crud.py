from sqlalchemy.orm import Session

from models import Plant
from schemas import PlantData

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
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