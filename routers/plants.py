from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas
import crud

router = APIRouter(tags=["Plants"])


@router.post("/users/{user_id}/plants/", response_model=schemas.Plant, status_code=201)
def create_plant_for_user(
    user_id: int, category_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_plant(db=db, plant=plant, user_id=user_id, category_id=category_id)


@router.get("/users/{user_id}/plants", response_model=list[schemas.Plant])
def read_plants_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plants = crud.get_plants_for_user(
        db, skip=skip, limit=limit, user_id=user_id)
    return plants


@router.get("/users/{user_id}/plants/{plant_id}", response_model=schemas.Plant)
def read_plant(
    plant_id: int, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db_plant


@router.patch("/users/{user_id}/plants/{plant_id}", response_model=schemas.Plant)
def update_plant_for_user(user_id: int, plant_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)
                          ):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.update_user_plant(db=db, plant_id=plant_id, plant=plant)


@router.delete("/users/{user_id}/plants/{plant_id}", response_model=schemas.Plant)
def delete_plant_for_user(user_id: int, plant_id: int, db: Session = Depends(get_db)
                          ):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.delete_user_plant_by_id(db=db, plant_id=plant_id)
