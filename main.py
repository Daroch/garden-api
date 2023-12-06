import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from celery import shared_task, Celery


from celery_config import settings

import models
from routers import alerts, alerttypes, categories, journals, plants, users
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

app.mount("/images",
          StaticFiles(directory="images"), name='images')

allow_origin = os.getenv('ALLOW_ORIGIN')
origin = allow_origin.split(',') if allow_origin else [
    'http://localhost:3000', 'http://localhost:5173']

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


@celery.task
def send_push_notification(device_token: str):
    time.sleep(10)  # simulates slow network call to firebase/sns
    with open("notification.log", mode="a") as notification_log:
        response = f"Successfully sent push notification to: {device_token}\n"
        notification_log.write(response)


@app.get("/push/{device_token}")
async def notify(device_token: str):
    send_push_notification.delay(device_token)
    return {"message": "Notification sent"}
