from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import logging

from app.database import get_db, engine, Base
from app.schemas import AdviceRequest, AdviceResponse
from app.crud import get_crop_optimal, get_readings_by_crop, save_reading
from app.advice_generator import generate_advice
from app.load_csv import load_csv_data
from app.config import API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agriculture Advisory API", version="1.0")

async def verify_api_key(x_api_key: str = Depends(lambda: None)):
    # FastAPI can read header directly; easier to use Header param in endpoint
    pass

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Load CSV data
    await load_csv_data()
    logger.info("Startup complete.")

@app.get("/api/v1/advice", response_model=AdviceResponse)
async def get_advice(
    crop_type: str = Query(..., min_length=1, max_length=100),
    soil_moisture: float = Query(..., ge=0.0, le=100.0),
    temperature: float = Query(..., ge=-10.0, le=60.0),
    humidity: float = Query(..., ge=0.0, le=100.0),
    co2_level: float = Query(..., ge=300.0, le=5000.0),
    is_greenhouse: bool = Query(...),
    x_api_key: str = None,  # reading from header
    db: AsyncSession = Depends(get_db)
):
    # API Key check
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing X-API-Key")
    
    # Normalize crop_type
    crop_type_norm = crop_type.strip().lower()
    
    # Fetch optimal ranges from DB
    optimal = await get_crop_optimal(db, crop_type_norm, is_greenhouse)
    if not optimal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No optimal data found for crop '{crop_type}' with greenhouse={is_greenhouse}"
        )
    
    measured = {
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "co2_level": co2_level,
    }
    
    advice_text = generate_advice(crop_type_norm, is_greenhouse, measured, optimal)
    
    await save_reading(db, {
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

@app.get("/api/v1/history/{crop_type}")
async def get_history(
    crop_type: str,
    x_api_key: str = None,
    db: AsyncSession = Depends(get_db)
):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    readings = await get_readings_by_crop(db, crop_type.lower())
    
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")
    
    return readings