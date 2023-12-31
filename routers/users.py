from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas import User, UserCreate, Token, Plant
import crud
import auth

router = APIRouter(tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = auth.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def get_my_details(current_user: Annotated[User, Depends(auth.get_current_active_user)]):
    return current_user


@router.post("/users/", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_new_user = crud.create_user(db=db, user=user)
    return db_new_user


@router.get("/users/", response_model=list[User])
def get_all_users(current_user: Annotated[User, Security(
        auth.get_current_active_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if current_user.name != "admin":
        raise HTTPException(
            status_code=403, detail="Only admin can delete Users")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", response_model=User)
def delete_user(current_user: Annotated[User, Security(
        auth.get_current_active_user)], user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.name != "admin":
        raise HTTPException(
            status_code=403, detail="Only admin can delete Users")
    db_user = crud.delete_user_by_id(db, user_id=user_id)
    return db_user
