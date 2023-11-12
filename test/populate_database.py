from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_populate():
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    data = response.json()
    if data:
        raise HTTPException(status_code=404, detail="Ya existen datos!!")
    user1 = {
        "email": "frodo@gmail.com",
        "name": "Frodo",
        "hashed_password": "12345"
    }
    user2 = {
        "email": "gandalf@gmail.com",
        "name": "Gandalf",
        "hashed_password": "12345"
    }
    user3 = {
        "email": "Saruman@gmail.com",
        "name": "Saruman",
        "hashed_password": "12345"
    }
    category1 = {
        "name": "Ornamentales",
        "description": "Plantas ornamentales y flores en general"
    }
    category2 = {
        "name": "Huerta",
        "description": "Plantas comestibles de la huerta"
    }
    plant1 = {
        "name": "Aloe Vera",
        "description": "planta medicinal",
        "public": True,
        "irrigation_type": "muypoca",
        "light_type": "poca",
        "location": "balcón",
        "notes": "string",
        "image": "string"
    }
    plant2 = {
        "name": "Ficus",
        "description": "planta muy longeva y agradecida",
        "public": True,
        "irrigation_type": "bastante",
        "light_type": "poca",
        "location": "interior",
        "notes": "string",
        "image": "string"
    }
    plant3 = {
        "name": "Albahaca",
        "description": "Especia para salsas y aderezos",
        "public": True,
        "irrigation_type": "bastante",
        "light_type": "poca",
        "location": "interior",
        "notes": "string",
        "image": "string"
    }
    journal1 = {
        "title": "Transplante en noviembre",
        "description": "transplantada a maceta de 20l",
        "image": "string"
    }
    journal2 = {
        "title": "Poda 2023",
        "description": "Retiradas hojas muertas",
        "image": "string"
    }
    alert_type1 = {
        "alert_name": "Riego"
    }
    alert_type2 = {
        "alert_name": "Abono"
    }
    alert1 = {
        "notes": "riego1",
        "start_date": "2023-11-10T00:04:44.601Z",
        "status": True,
        "repeat": True,
        "frecuency": 3
    }
    alert2 = {
        "notes": "riego2",
        "start_date": "2023-11-10T00:04:44.601Z",
        "status": True,
        "repeat": True,
        "frecuency": 5
    }
    alert3 = {
        "notes": "riego3",
        "start_date": "2023-11-10T00:04:44.601Z",
        "status": True,
        "repeat": True,
        "frecuency": 10
    }
    response = client.post("/users/",json=user1)
    response = client.post("/users/",json=user2)
    response = client.post("/users/",json=user3)
    response = client.post("/categories/",json=category1)
    response = client.post("/categories/",json=category2)
    response = client.post("/users/1/plants?category_id=1",json=plant1)
    response = client.post("/users/1/plants?category_id=1",json=plant2)
    response = client.post("/users/2/plants?category_id=2",json=plant3)
    response = client.post("/users/1/plants/1/journals",json=journal1)
    response = client.post("/users/1/plants/1/journals",json=journal2)
    response = client.post("/alert_types/",json=alert_type1)
    response = client.post("/alert_types/",json=alert_type2)
    response = client.post("/users/1/plants/1/alerts?alert_type_id=1",json=alert1)
    response = client.post("/users/1/plants/1/alerts?alert_type_id=1",json=alert2)
    response = client.post("/users/1/plants/3/alerts?alert_type_id=1",json=alert3)
    return 'Hecho, datos añadidos!'
