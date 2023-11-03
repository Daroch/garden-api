from sqlalchemy import Column, String, Integer, Enum, DATETIME, Boolean

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    plants = relationship("Plant", back_populates="owner")
class Plant(Base):
  __tablename__ = 'plants'
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(30), index=True)
  description = Column(String(300))
  publish = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))
  
  owner = relationship("User", back_populates="plants")
