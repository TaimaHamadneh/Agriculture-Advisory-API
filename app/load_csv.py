import csv
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CropOptimal
from app.database import AsyncSessionLocal

async def load_csv_data():
    async with AsyncSessionLocal() as session:

        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(CropOptimal))
        count = result.scalar()
        if count > 0:
            print("Data already loaded, skipping CSV import.")
            return

        with open("crop_optimal_conditions.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append(CropOptimal(
                    label=row["label"].lower(),
                    in_greenhouse=row["in_greenhouse"].lower() == "true",
                    temp_min=float(row["temp_min"]),
                    temp_max=float(row["temp_max"]),
                    humidity_min=float(row["humidity_min"]),
                    humidity_max=float(row["humidity_max"]),
                    co2_min=float(row["co2_min"]),
                    co2_max=float(row["co2_max"]),
                    soil_moisture_min=float(row["soil_moisture_min"]),
                    soil_moisture_max=float(row["soil_moisture_max"]),
                ))
            session.add_all(rows)
            await session.commit()
            print(f"Loaded {len(rows)} crop optimal records.")