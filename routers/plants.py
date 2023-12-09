import os
from pathvalidate import sanitize_filename
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
    current_user: Annotated[User, Security(
        auth.get_current_active_user)],
    user_id: int,
    category_id: int = Form(...),
    imagefile: Annotated[UploadFile,
                         File(..., description="Main image for your Plant")] = None,
    name: str = Form(...),
    description: str = Form(None),
    plant_public: bool = Form(...),
    irrigation_type: str = Form(...),
    light_type: str = Form(...),
    location: str = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db)
):
    plant = PlantCreate(name=name, description=description, category_id=category_id, plant_public=plant_public,
                        irrigation_type=irrigation_type, light_type=light_type, location=location, notes=notes)
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This is not your user")
    if imagefile:
        # create a folder with next id and sanitize filename
        next_plant_id = crud.get_plant_latest_id(db=db)+1
        folder = "images/plants/" + str(user_id) + "/" + str(next_plant_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        clean_name = sanitize_filename(imagefile.filename)
        with open(folder + "/" + clean_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        plant.image_url = clean_name
    else:
        plant.image_url = ""

    return crud.create_user_plant(db=db, plant=plant, user_id=user_id)


@router.get("/users/{user_id}/plants", response_model=list[Plant])
def get_plants_for_user(current_user: Annotated[User, Security(
        auth.get_current_active_user)], user_id: int, search_text: str = '', search_category_id: int = 0, db: Session = Depends(get_db)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This is not your user")
    db_plants = crud.get_plants_for_user(
        db, user_id, search_text, search_category_id)
    return db_plants


@router.get("/plants", response_model=list[Plant])
async def get_all_plants_for_explore_search(
    search_text: str = '', search_category_id: int = 0, db: Session = Depends(get_db)
):
    db_plants = crud.get_all_plants_for_explore_search(
        db, search_text, search_category_id)
    return db_plants


@router.get("/users/{user_id}/plants/{plant_id}", response_model=Plant)
def get_plant_details(
    plant_id: int, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant_details(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return db_plant


@router.patch("/users/{user_id}/updateplant/{plant_id}", response_model=Plant)
async def update_plant(
        current_user: Annotated[User, Security(
        auth.get_current_active_user)],
        user_id: int,
        plant_id: int,
        category_id: int = Form(...),
        imagefile: Annotated[UploadFile,
                             File(..., description="Main image for your Plant")] = None,
        name: str = Form(...),
        description: str = Form(None),
        plant_public: bool = Form(...),
        irrigation_type: str = Form(...),
        light_type: str = Form(...),
        location: str = Form(None),
        notes: str = Form(None),
        image_url: str = Form(None),
        db: Session = Depends(get_db)
):
    plant = PlantCreate(name=name, description=description, category_id=category_id, plant_public=plant_public,
                        irrigation_type=irrigation_type, light_type=light_type, location=location, notes=notes, image_url=image_url)

    db_plant = crud.get_plant_details(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if current_user.id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    if imagefile:
        # Verify a folder and sanitize filename
        folder = "images/plants/" + str(user_id) + "/" + str(plant_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        clean_name = sanitize_filename(imagefile.filename)
        with open(folder + "/" + clean_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        plant.image_url = clean_name
    else:
        if plant.image_url == "null":
            plant.image_url = ""
    return crud.update_user_plant(db=db, plant_id=plant_id, plant=plant)


@router.delete("/users/{user_id}/plants/{plant_id}", response_model=Plant)
def delete_plant(current_user: Annotated[User, Security(
    auth.get_current_active_user)],
    user_id: int, plant_id: int, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant_details(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if current_user.id is not db_plant.owner_id:
        raise HTTPException(status_code=500, detail="This is not your plant")
    return crud.delete_user_plant_by_id(db=db, plant_id=plant_id)
