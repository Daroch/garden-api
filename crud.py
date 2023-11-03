from sqlalchemy.orm import Session

from models import User, Plant, Category
from schemas import UserCreate, PlantCreate, CategoryCreate

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

def create_user_plant(db: Session, plant: PlantCreate, user_id: int, category_id: int):
    db_plant = Plant(**plant.dict(), owner_id=user_id, category_id=category_id)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def get_categories(db: Session, skip: int = 0, limit: int = 100):
   return db.query(Category).offset(skip).limit(limit).all()

def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category