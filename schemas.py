from pydantic import BaseModel, EmailStr
import models

class JournalBase(BaseModel):
    title: str
    description: str | None = None
    image: str | None = None

class JournalCreate(JournalBase):
    pass

class Journal(JournalBase):
    id: int
    plant_id: int
    created_at: str

    class Config:
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
    created_at: str

    class Config:
        from_attributes = True



class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    plants: list[Plant] = []

    class Config:
        from_attributes = True



class UserBase(BaseModel):
    email: EmailStr
    name: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    plants: list[Plant] = []

    class Config:
        from_attributes = True
        
