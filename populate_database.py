from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def read_main():
    response = client.get("/")
    return response

@app.get("/populate")
def populate_data(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    if users:
        raise HTTPException(status_code=404, detail="Ya existen datos!!")
    user1 = {
        "email": "frodo@gmail.com",
        "name": "Frodo",
        "password": "12345"
    }
    user2 = {
        "email": "gandalf@gmail.com",
        "name": "Gandalf",
        "password": "12345"
    }
    user3 = {
        "email": "Saruman@gmail.com",
        "name": "Saruman",
        "password": "12345"
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
   #db_user = User(email=user.email, name=user.name,
    #               hashed_password=fake_hashed_password)
    create_user(db=db,user=json.dumps(user1))
    crud.create_user(db=db, user=user2)
    crud.create_user(db=db, user=user3)
    crud.create_category(db=db, category=category1)
    crud.create_category(db=db, category=category2)
    crud.create_user_plant(db=db, plant=plant1, user_id=1, category_id=1)
    crud.create_user_plant(db=db, plant=plant2, user_id=1, category_id=1)
    crud.create_user_plant(db=db, plant=plant3, user_id=2, category_id=2)
    crud.create_journal_plant(db=db, journal=journal1, plant_id=1)
    crud.create_journal_plant(db=db, journal=journal2, plant_id=1)
    crud.create_alert_type(db=db, alert_type=alert_type1)
    crud.create_alert_type(db=db, alert_type=alert_type2)
    crud.create_alert_plant(db=db, alert=alert1, plant_id=1, alert_type_id=1)
    crud.create_alert_plant(db=db, alert=alert2, plant_id=3, alert_type_id=2)
    crud.create_alert_plant(db=db, alert=alert3, plant_id=3, alert_type_id=1)
    return 'Hecho, datos añadidos!'
