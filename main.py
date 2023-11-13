from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from routers import alerts, alerttypes, categories, journals, plants, users
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origin = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.include_router(alerts.router)
app.include_router(alerttypes.router)
app.include_router(categories.router)
app.include_router(journals.router)
app.include_router(plants.router)
app.include_router(users.router)


@app.get('/')
def root():
    return {"msg": "Hello, I am FastAPI"}
