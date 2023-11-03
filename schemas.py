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
        
class PlantData(BaseModel):
  name: str
  description: str
  publish: bool

class PlantId(PlantData):
  id: int
  
