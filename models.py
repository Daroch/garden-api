import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(50), index=True)
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
    muypoca = "muypoca"
    poca = "poca"
    normal = "normal"
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
  description = Column(String(300), index=True, nullable= True)
  public = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  category_id = Column(Integer, ForeignKey("categories.id"))
  irrigation_type = Column(Enum('muypoca','poca','normal','bastante','mucha'), name='irrigation_type', nullable= False, default=IrrigationType.muypoca)
  light_type = Column(Enum('muypoca','poca','normal','bastante','mucha'), name='light_type', nullable= False, default=LightType.muypoca)
  location = Column(String(30), nullable=True)
  notes = Column(String(500), nullable=True)
  image = Column(String(120), nullable= True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  
  journals = relationship("Journal",back_populates="plant")

  owner = relationship("User", back_populates="plants")
  category = relationship("Category", back_populates="plants")

class Journal(Base):
  __tablename__ = "journals"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(100), index=True)
  description = Column(String(500), index=True, nullable= True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  image = Column(String(120), nullable= True)
  plant_id = Column(Integer, ForeignKey("plants.id"), nullable= False)

  plant = relationship("Plant", back_populates="journals")
