from typing import Annotated
from fastapi import APIRouter, Depends, Security, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

from dependencies import get_db

from schemas import User, Plant, PlantCreate
import crud
import auth


router = APIRouter(tags=["Plants"])


@router.post("/users/{user_id}/addplant", response_model=Plant, status_code=201)
async def create_plant(
    user_id: int,
    category_id: int = Form(...),
    imagefile: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    public: bool = True,
    irrigation_type: str = Form(...),
    light_type: str = Form(...),
    db: Session = Depends(get_db)
):
    plant = PlantCreate(owner_id=user_id, name=name, category_id=category_id, public=public,
                        irrigation_type=irrigation_type, light_type=light_type, description=description)
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if imagefile:
        new_name = "_".join([str(user_id), "_".join(
            plant.name.split()), imagefile.filename])
        with open("images/plants/" + new_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        plant.image_url = new_name

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


@router.patch("/users/{user_id}/updateplant/{plant_id}", response_model=Plant)
async def update_plant(
        user_id: int,
        plant_id: int,
        imagefile: Annotated[UploadFile,
                             File(..., description="Main image for your Plant")] = None,
        plant: PlantCreate = Depends(),
        db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if user_id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    if imagefile:
        new_name = "_".join([str(user_id), "_".join(
            plant.name.split()), imagefile.filename])
        with open("images/plants/" + new_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        plant.image_url = new_name
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
