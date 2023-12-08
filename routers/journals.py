import os
from pathvalidate import sanitize_filename
from typing import Annotated
from fastapi import APIRouter, Depends, Security, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import Journal, JournalCreate
import crud
import shutil

router = APIRouter(tags=["Journals"])


@router.get("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=Journal)
def get_journal_details(
    journal_id: int, db: Session = Depends(get_db)
):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    return db_journal


@router.get("/users/{user_id}/plants/{plant_id}/journals", response_model=list[Journal])
def get_journals_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.get_journals_for_plant(
        db, skip=skip, limit=limit, plant_id=plant_id)
    return journals


@router.get("/users/{user_id}/journals", response_model=list[Journal])
def get_journals_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.get_journals_for_user(
        db, skip=skip, limit=limit, user_id=user_id)
    return journals


@router.post("/users/{user_id}/plants/{plant_id}/addjournal", response_model=Journal, status_code=201)
def create_journal_for_plant(
        user_id: int,
        plant_id: int,
        imagefile: Annotated[UploadFile,
                             File(..., description="Main image for your Journal")] = None,
        title: str = Form(...),
        description: str = Form(None), db: Session = Depends(get_db)):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    journal = JournalCreate(title=title, description=description)
    if imagefile:
        # create a folder with next id and sanitize filename
        next_journal_id = crud.get_journal_latest_id(db=db)+1
        folder = "images/plants/" + \
            str(user_id) + "/" + str(plant_id) + "/" + str(next_journal_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        clean_name = sanitize_filename(imagefile.filename)
        with open(folder + "/" + clean_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        journal.image_url = clean_name
    else:
        journal.image_url = ""

    db_journal = crud.create_journal_plant(
        db=db, journal=journal, plant_id=plant_id)
    return db_journal


@router.patch("/users/{user_id}/plants/{plant_id}/updatejournal/{journal_id}", response_model=Journal)
def update_journal(
        user_id: int,
        plant_id: int,
        journal_id: int,
        imagefile: Annotated[UploadFile,
                             File(..., description="Main image for your Journal")] = None,
        title: str = Form(...),
        description: str = Form(None),
        image_url: str = Form(None),
        db: Session = Depends(get_db)):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    journal = JournalCreate(
        title=title, description=description, image_url=image_url)
    if imagefile:
        # Verify a folder and sanitize filename
        folder = "images/plants/" + \
            str(user_id) + "/" + str(plant_id) + "/" + str(journal_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        clean_name = sanitize_filename(imagefile.filename)
        with open(folder + "/" + clean_name, "wb") as buffer:
            shutil.copyfileobj(imagefile.file, buffer)
        journal.image_url = clean_name
    else:
        if journal.image_url == "null":
            journal.image_url = ""
    return crud.update_journal_plant(db=db, journal_id=journal_id, journal=journal)


@router.delete("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=Journal)
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    db_journal = crud.delete_journal_by_id(db, journal_id=journal_id)
    return db_journal
