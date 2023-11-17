from typing import Annotated
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import User, Plant, PlantCreate
import crud
import auth

router = APIRouter(tags=["Plants"])


@router.post("/users/{user_id}/plants/", response_model=Plant, status_code=201)
def create_plant(
    user_id: int, category_id: int, plant: PlantCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_plant(db=db, plant=plant, user_id=user_id, category_id=category_id)


@router.get("/users/{user_id}/plants", response_model=list[Plant])
def get_plants_for_user(current_user: Annotated[User, Security(
        auth.get_current_active_user, scopes=["plants"])], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plants = crud.get_plants_for_user(
        db, skip=skip, limit=limit, user_id=current_user.id)
    return plants


@router.get("/plants", response_model=list[Plant])
def get_all_plants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plants = crud.get_plants(
        db, skip=skip, limit=limit)
    return plants


@router.get("/users/{user_id}/plants/{plant_id}", response_model=Plant)
def get_plant_details(
    plant_id: int, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db_plant


@router.patch("/users/{user_id}/plants/{plant_id}", response_model=Plant)
def update_plant(user_id: int, plant_id: int, plant: PlantCreate, db: Session = Depends(get_db)
                 ):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.update_user_plant(db=db, plant_id=plant_id, plant=plant)


@router.delete("/users/{user_id}/plants/{plant_id}", response_model=Plant)
def delete_plant(user_id: int, plant_id: int, db: Session = Depends(get_db)
                 ):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.delete_user_plant_by_id(db=db, plant_id=plant_id)
