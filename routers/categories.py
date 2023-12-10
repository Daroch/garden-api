from typing import Annotated
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import Category, User, CategoryCreate
import crud
import auth

router = APIRouter(tags=["Categories"])


@router.get("/categories", response_model=list[Category])
def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.post("/addcategory", response_model=Category, status_code=201)
def create_category(current_user: Annotated[User, Security(
        auth.get_current_active_user)], category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="category already exists")
    if current_user.name != "admin":
        raise HTTPException(
            status_code=403, detail="Only admin can create New Categories")
    return crud.create_category(db=db, category=category)
