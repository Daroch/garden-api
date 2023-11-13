from datetime import datetime
from pydantic import BaseModel, EmailStr
import models


class AlertBase(BaseModel):
    notes: str | None = None
    start_date: datetime
    status: bool
    repeat: bool
    frecuency: int


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    created_at: datetime
    plant_id: int
    alert_type_id: int

    class ConfigDict:
        from_attributes = True


class AlertTypeBase(BaseModel):
    alert_name: str


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
    image: str | None = None


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
    public: bool
    irrigation_type: str = models.IrrigationType.muypoca
    light_type: str = models.LightType.muypoca
    location: str | None = None
    notes: str | None = None
    image: str | None = None


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int
    owner_id: int
    category_id: int
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
