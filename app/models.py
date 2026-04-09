from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base
from datetime import datetime

class CropOptimal(Base):
    __tablename__ = "crop_optimal_conditions"

    label = Column(String, primary_key=True)
    in_greenhouse = Column(Boolean, primary_key=True)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity_min = Column(Float)
    humidity_max = Column(Float)
    co2_min = Column(Float)
    co2_max = Column(Float)
    soil_moisture_min = Column(Float)
    soil_moisture_max = Column(Float)


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_type = Column(String, nullable=False)
    is_greenhouse = Column(Boolean, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    co2_level = Column(Float, nullable=False)
    soil_moisture = Column(Float, nullable=False)
    advice = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)