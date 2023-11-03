from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    plants: list[Plant] = []

    class Config:
        orm_mode = True
        
class PlantBase(BaseModel):
    name: str
    description: str | None = None
    public: bool

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
  