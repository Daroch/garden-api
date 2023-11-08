from datetime import datetime
from sqlalchemy.orm import Session

from models import User, Plant, Category, Journal
from schemas import UserCreate, PlantCreate, CategoryCreate, JournalCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, name=user.name,
                   hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_plant(db: Session, plant_id: int):
    return db.query(Plant).filter(Plant.id == plant_id).first()


def get_plants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Plant).offset(skip).limit(limit).all()


def get_plants_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Plant).filter(Plant.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_plant(db: Session, plant: PlantCreate, user_id: int, category_id: int):
    db_plant= Plant(**plant.dict(), owner_id=user_id, category_id=category_id, created_at=datetime.now())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


def update_user_plant(db: Session, plant_id: int, plant: PlantCreate):
    db_plant= get_plant(db, plant_id=plant_id)
    for key, value in plant:
        setattr(db_plant, key, value)
    db.commit()
    return db_plant


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_journal(db: Session, journal_id: int):
    return db.query(Journal).filter(Journal.id == journal_id).first()

def get_journals_for_plant(db: Session, plant_id: int, skip: int = 0, limit: int = 100):
    return db.query(Journal).filter(Journal.plant_id == plant_id).offset(skip).limit(limit).all()

def create_journal_plant(db: Session, journal: JournalCreate, plant_id: int):
    db_journal = Journal(**journal.dict(), plant_id=plant_id, created_at=datetime.now())
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal

def update_plant_journal(db: Session, journal_id: int, journal: JournalCreate):
    db_journal= get_journal(db, journal_id=journal_id)
    for key, value in journal:
        setattr(db_journal, key, value)
    db.commit()
    return db_journal