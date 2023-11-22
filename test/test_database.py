from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


from database import TEST_URL_CONNECTION, Base
import models
from main import app
from dependencies import get_db


Testingengine = create_engine(TEST_URL_CONNECTION)
TestingSessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=Testingengine)

models.Base.metadata.create_all(bind=Testingengine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

db = override_get_db()
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, I am FastAPI"}


def test_create_user_ok():
    user = {
        "email": "frodo@gmail.com",
        "name": "Frodo",
        "hashed_password": "12345"
    }
    response = client.post("/users/", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['email'] == user['email']
    assert data['name'] == user['name']
    response2 = client.delete(f"users/{data['id']}")


def test_create_user_duplicate_email():
    user = {
        "email": "frodo@gmail.com",
        "name": "Frodo",
        "hashed_password": "12345"
    }
    response = client.post("/users/", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    response = client.post("/users/", json=user)
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Email already registered"}
    response = client.delete(f"users/{data['id']}")
