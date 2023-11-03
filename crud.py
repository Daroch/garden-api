from sqlalchemy.orm import Session

from models import User, Plant
from schemas import UserCreate, PlantCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
def get_plants(db: Session, skip: int = 0, limit: int = 100):
   return db.query(Plant).offset(skip).limit(limit).all()

def create_user_plant(db: Session, plant: PlantCreate, user_id: int):
    db_new_plant = Plant(**plant.dict(), owner_id=user_id)
    db.add(db_new_plant)
    db.commit()
    db.refresh(db_new_plant)
    return db_new_plant