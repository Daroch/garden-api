from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from schemas import UserCreate
from models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_userDB_by_name(db: Session, name: str):
    return db.query(UserCreate).filter(UserCreate.name == name).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_userDB_by_name(db=db, name=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
