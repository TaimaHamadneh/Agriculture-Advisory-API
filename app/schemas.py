from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class AdviceRequest(BaseModel):
    crop_type: str = Field(..., min_length=1, max_length=100)
    soil_moisture: float = Field(..., ge=0.0, le=100.0)
    temperature: float = Field(..., ge=-10.0, le=60.0)
    humidity: float = Field(..., ge=0.0, le=100.0)
    co2_level: float = Field(..., ge=300.0, le=5000.0)
    is_greenhouse: bool

    @field_validator("crop_type")
    def lowercase_crop(cls, v: str) -> str:
        return v.strip().lower()

class AdviceResponse(BaseModel):
    crop_type: str
    is_greenhouse: bool
    conditions: dict
    advice: str
    generated_at: datetime