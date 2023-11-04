from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DATETIME, Boolean
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_active = Column(Boolean, default=True)

    plants = relationship("Plant", back_populates="owner")


class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(30), unique=True, index=True)
  description = Column(String(300), index=True)

  plants = relationship("Plant", back_populates="category")


class LevelType(str, Enum):
    muypoca = "muy poca"
    poca = "poca"
    bastante = "bastante"
    mucha = "mucha"

class IrrigationType(LevelType):
  pass

class LightType(LevelType):
  pass



class Plant(Base):
  __tablename__ = 'plants'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(30), index=True)
  description = Column(String(300), index=True)
  public = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  category_id = Column(Integer, ForeignKey("categories.id"))
  irrigation_type = Column(IrrigationType)
  light_type = Column(LightType)

  owner = relationship("User", back_populates="plants")
  category = relationship("Category", back_populates="plants")
  

