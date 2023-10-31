from sqlalchemy import Column, String, Integer, Enum, DATETIME, Boolean

from database import Base

class Plant(Base):
  __tablename__ = 'plants'
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(30), index=True)
  description = Column(String(300))
  publish = Column(Boolean, default=False)
