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
class Plant(Base):
  __tablename__ = 'plants'
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(30), index=True)
  description = Column(String(300), index=True)
  public = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  
  owner = relationship("User", back_populates="plants")
