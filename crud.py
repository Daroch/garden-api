from datetime import datetime
from sqlalchemy.orm import Session

from models import User, Plant, Category, Journal, AlertType, Alert
from schemas import UserCreate, PlantCreate, CategoryCreate, JournalCreate, AlertTypeCreate, AlertCreate

import auth


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = auth.get_password_hash(user.hashed_password)
    db_user = User(email=user.email, name=user.name,
                   hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_plant(db: Session, plant_id: int):
    return db.query(Plant).filter(Plant.id == plant_id).first()


def get_plants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Plant).offset(skip).limit(limit).all()


def get_plants_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Plant).filter(Plant.owner_id == user_id).offset(skip).limit(limit).all()


def get_plant_latest_id(db: Session):
    return db.query(Plant).order_by(Plant.id.desc()).first().id


def create_user_plant(db: Session, plant: PlantCreate, user_id: int):
    db_plant = Plant(**plant.dict(), owner_id=user_id,
                     created_at=datetime.now())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


def update_user_plant(db: Session, plant_id: int, plant: PlantCreate):
    db_plant = get_plant(db, plant_id=plant_id)
    for key, value in plant:
        setattr(db_plant, key, value)
    db.commit()
    return db_plant


def delete_user_plant_by_id(db: Session, plant_id: int):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    db.delete(db_plant)
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


def delete_category_by_id(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category


def get_journal(db: Session, journal_id: int):
    return db.query(Journal).filter(Journal.id == journal_id).first()


def get_journals_for_plant(db: Session, plant_id: int, skip: int = 0, limit: int = 100):
    return db.query(Journal).filter(Journal.plant_id == plant_id).offset(skip).limit(limit).all()


def create_journal_plant(db: Session, journal: JournalCreate, plant_id: int):
    db_journal = Journal(**journal.dict(), plant_id=plant_id,
                         created_at=datetime.now())
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal


def update_journal_plant(db: Session, journal_id: int, journal: JournalCreate):
    db_journal = get_journal(db, journal_id=journal_id)
    for key, value in journal:
        setattr(db_journal, key, value)
    db.commit()
    return db_journal


def delete_journal_by_id(db: Session, journal_id: int):
    db_journal = db.query(Journal).filter(Journal.id == journal_id).first()
    db.delete(db_journal)
    db.commit()
    return db_journal


def get_alert_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AlertType).offset(skip).limit(limit).all()


def get_alert_type_by_name(db: Session, alert_name: str):
    return db.query(AlertType).filter(AlertType.alert_name == alert_name).first()


def create_alert_type(db: Session, alert_type: AlertTypeCreate):
    db_alert_type = AlertType(
        alert_name=alert_type.alert_name)
    db.add(db_alert_type)
    db.commit()
    db.refresh(db_alert_type)
    return db_alert_type


def get_alert(db: Session, alert_id: int):
    return db.query(Alert).filter(Alert.id == alert_id).first()


def get_alerts_for_plant(db: Session, plant_id: int, skip: int = 0, limit: int = 100):
    return db.query(Alert).filter(Alert.plant_id == plant_id).offset(skip).limit(limit).all()


def get_alerts_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Alert).join(Plant).filter(Plant.owner_id == user_id).offset(skip).limit(limit).all()


def create_alert_plant(db: Session, alert: AlertCreate, plant_id: int):
    db_alert = Alert(**alert.dict(), plant_id=plant_id,
                     created_at=datetime.now())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def update_alert_plant(db: Session, alert_id: int, alert: AlertCreate):
    db_alert = get_alert(db, alert_id=alert_id)
    for key, value in alert:
        setattr(db_alert, key, value)
    db.commit()
    return db_alert


def delete_alert_by_id(db: Session, alert_id: int):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    db.delete(db_alert)
    db.commit()
    return db_alert


def get_all_alerts_to_send_email(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Alert).filter(Alert.start_date < datetime.now()).join(Plant).join(User).all()


def get_all_alerts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Alert).join(Plant).join(User).all()


def get_prueba(db: Session, skip: int = 0, limit: int = 100):
    for u, p, a in db.query(User, Plant, Alert).filter(User.id == Plant.owner_id).filter(Plant.id == Alert.plant_id).all():
        listofusers = [u]
        listofplants = [p]
        listofalerts = [a]
        return listofusers, listofplants, listofalerts
