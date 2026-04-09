import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://agri_user:agri_pass@localhost:5432/agri_db")
API_KEY = os.getenv("API_KEY", "default-dev-key-change-me")