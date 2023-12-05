import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    plants = relationship("Plant", back_populates="owner",
                          cascade='all,delete')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True, nullable=False)
    description = Column(String(300), index=True, nullable=True)

    plants = relationship("Plant", back_populates="category")

#


class LevelType(str, Enum):
    level1 = "level1"
    level1 = "level2"
    level3 = "level3"
    level4 = "level4"
    level5 = "level5"


class IrrigationType(LevelType):
    pass


class LightType(LevelType):
    pass


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True, nullable=False)
    description = Column(String(300), index=True, nullable=True)
    plant_public = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    irrigation_type = Column(Enum('level1', 'level2', 'level3', 'level4', 'level5', name='irrigation_type'),
                             name='irrigation_type', nullable=False, default=IrrigationType.level3)
    light_type = Column(Enum('level1', 'level2', 'level3', 'level4', 'level5', name='light_type'),
                        name='light_type', nullable=False, default=LightType.level3)
    location = Column(String(30), nullable=True)
    notes = Column(String(500), nullable=True)
    image_url = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    journals = relationship(
        "Journal", back_populates="plant", cascade="all,delete")
    alerts = relationship("Alert", back_populates="plant",
                          cascade="all,delete")

    owner = relationship("User", back_populates="plants")
    category = relationship("Category", back_populates="plants")


class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False, default=func.now())
    description = Column(String(500), index=True, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    image_url = Column(String(120), nullable=True)
    plant_id = Column(Integer, ForeignKey(
        "plants.id", ondelete="CASCADE"), nullable=False)

    plant = relationship("Plant", back_populates="journals")


class AlertType(Base):
    __tablename__ = "alert_types"

    id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String(30), unique=True, index=True, nullable=False)
    alert_description = Column(String(200), index=True, nullable=True)

    alerts = relationship("Alert", back_populates="alert_type")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    notes = Column(String(200), index=True, nullable=True)
    title = Column(String(100), index=True, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    start_date = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    repeat = Column(Boolean, default=True, nullable=False)
    frecuency = Column(Integer, nullable=True)
    alert_type_id = Column(Integer, ForeignKey(
        "alert_types.id"), nullable=False)
    plant_id = Column(Integer, ForeignKey(
        "plants.id", ondelete="CASCADE"), nullable=False)

    alert_type = relationship("AlertType", back_populates="alerts")
    plant = relationship("Plant", back_populates="alerts")
