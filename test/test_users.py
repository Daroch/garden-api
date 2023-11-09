from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, I am FastAPI"}

def test_create_user_ok():
    user = {
  "email": "frodo@gmail.com",
  "name": "Frodo",
  "password": "12345"
}
    response = client.post("/users/",json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['email'] == user['email']
    assert data['name'] == user['name']

def test_create_user_duplicate():
    user = {
  "email": "frodo@gmail.com",
  "name": "Frodo",
  "password": "12345"
}
    response = client.post("/users/",json=user)
    assert response.status_code == 400, response.text
    data = response.json()
    assert response.json() == {"detail": "Email already registered"}