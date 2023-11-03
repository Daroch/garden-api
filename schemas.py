from pydantic import BaseModel

class PlantBase(BaseModel):
    name: str
    description: str | None = None
    public: bool

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase):
    id: int
    owner_id: int
    category_id: int

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
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    plants: list[Plant] = []

    class Config:
        from_attributes = True
        
