from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CropOptimal, SensorReading


async def get_crop_optimal(session: AsyncSession, crop_type: str, is_greenhouse: bool):
    stmt = select(CropOptimal).where(
        CropOptimal.label == crop_type,
        CropOptimal.in_greenhouse == is_greenhouse
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def save_reading(session: AsyncSession, data: dict, advice: str):
    reading = SensorReading(
        crop_type=data["crop_type"],
        is_greenhouse=data["is_greenhouse"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        co2_level=data["co2_level"],
        soil_moisture=data["soil_moisture"],
        advice=advice
    )
    session.add(reading)
    await session.commit()
    return reading

async def get_readings_by_crop(session: AsyncSession, crop_type: str):
    stmt = select(SensorReading)\
        .where(SensorReading.crop_type == crop_type)\
        .order_by(SensorReading.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()
