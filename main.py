from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import engine, localSession
from schemas import PlantData, PlantId
from models import Base

app = FastAPI()


@app.get('/')
def root():
    return 'Hello, I am FastAPI'
