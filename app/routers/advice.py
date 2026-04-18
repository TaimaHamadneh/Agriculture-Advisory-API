from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database import get_db
from app.schemas import AdviceResponse
from app.utils.advice_generator import generate_advice
from app import crud  
from app.config import API_KEY

router = APIRouter(prefix="/api/v1", tags=["advice"])

@router.get("/advice", response_model=AdviceResponse)
async def get_advice(
    crop_type: str = Query(..., min_length=1, max_length=100),
    soil_moisture: float = Query(..., ge=0.0, le=100.0),
    temperature: float = Query(..., ge=-10.0, le=60.0),
    humidity: float = Query(..., ge=0.0, le=100.0),
    co2_level: float = Query(..., ge=300.0, le=5000.0),
    is_greenhouse: bool = Query(...),
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing X-API-Key")

    crop_type_norm = crop_type.strip().lower()
    

    optimal = await crud.get_crop_optimal(db, crop_type_norm, is_greenhouse)
    if not optimal:
        raise HTTPException(
            status_code=400,
            detail=f"No optimal data found for crop '{crop_type}' with greenhouse={is_greenhouse}"
        )

    measured = {
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "co2_level": co2_level,
    }

    advice_text = generate_advice(crop_type_norm, is_greenhouse, measured, optimal)


    await crud.save_reading(db, {
        "crop_type": crop_type_norm,
        "is_greenhouse": is_greenhouse,
        "temperature": temperature,
        "humidity": humidity,
        "co2_level": co2_level,
        "soil_moisture": soil_moisture,
    }, advice_text)

    return AdviceResponse(
        crop_type=crop_type_norm,
        is_greenhouse=is_greenhouse,
        conditions=measured,
        advice=advice_text,
        generated_at=datetime.utcnow()
    )

@router.get("/history/{crop_type}")
async def get_history(
    crop_type: str,
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    readings = await crud.get_readings_by_crop(db, crop_type.lower())
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")
    return readings