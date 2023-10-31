from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import engine, localSession
from schemas import PlantData, PlantId
from models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get('/')
def root():
    return 'Hello, I am FastAPI'
