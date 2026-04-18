from fastapi import FastAPI
import logging
from app.database import engine, Base
from app.load_csv import load_csv_data
from app.routers import advice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agriculture Advisory API", version="1.0")


app.include_router(advice.router)

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await load_csv_data()
    logger.info("Startup complete.")

@app.get("/health")
async def health():
    return {"status": "ok"}