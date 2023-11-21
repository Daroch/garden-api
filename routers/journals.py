from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
import schemas
import crud

router = APIRouter(tags=["Journals"])


@router.get("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=schemas.Journal)
def get_journal_details(
    journal_id: int, db: Session = Depends(get_db)
):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    return db_journal


@router.get("/users/{user_id}/plants/{plant_id}/addjournal", response_model=list[schemas.Journal])
def get_all_journals_for_plant(plant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.journals_for_plant(
        db, skip=skip, limit=limit, plant_id=plant_id)
    return journals


@router.post("/users/{user_id}/plants/{plant_id}/journals", response_model=schemas.Journal, status_code=201)
def create_journal_for_plant(
    plant_id: int, journal: schemas.JournalCreate, db: Session = Depends(get_db)
):
    db_plant = crud.get_plant(db, plant_id=plant_id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_journal = crud.create_journal_plant(
        db=db, journal=journal, plant_id=plant_id)
    return db_journal


@router.patch("/users/{user_id}/plants/{plant_id}/updatejournal/{journal_id}", response_model=schemas.Journal)
def update_journal(plant_id: int, journal_id: int, journal: schemas.JournalCreate, db: Session = Depends(get_db)
                             ):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    if plant_id is not db_journal.plant_id:
        raise HTTPException(
            status_code=500, detail="This journal i snot for that plant")
    return crud.update_plant_journal(db=db, plant_id=plant_id, plant=plant)


@router.delete("/users/{user_id}/plants/{plant_id}/journals/{journal_id}", response_model=schemas.Journal)
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    db_journal = crud.delete_journal_by_id(db, journal_id=journal_id)
    return db_journal