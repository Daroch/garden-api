from datetime import datetime
from pydantic import BaseModel, EmailStr
import models


class AlertBase(BaseModel):
    alert_type_id: int = 1
    title: str | None = None
    notes: str | None = None
    start_date: datetime = datetime.now()
    status: bool = True
    repeat: bool = False
    frecuency: int | None = None


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    created_at: datetime
    plant_id: int

    class ConfigDict:
        from_attributes = True


class AlertTypeBase(BaseModel):
    alert_name: str
    alert_description: str | None = None


class AlertTypeCreate(AlertTypeBase):
    pass


class AlertType(AlertTypeBase):
    id: int
    alerts: list[Alert] = []

    class ConfigDict:
        from_attributes = True


class JournalBase(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None


class JournalCreate(JournalBase):
    pass


class Journal(JournalBase):
    id: int
    plant_id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class PlantBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    plant_public: bool = True
    irrigation_type: str = models.IrrigationType.level3
    light_type: str = models.LightType.level3
    location: str | None = None
    notes: str | None = None
    image_url: str | None = None


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int
    owner_id: int
    created_at: datetime
    journals: list[Journal] = []
    alerts: list[Alert] = []

    class ConfigDict:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    plants: list[Plant] = []

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    plants: list[Plant] = []

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
