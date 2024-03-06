import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "database")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "animegen")
DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SERVER_URL: str = "http://localhost:8000"

FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "image_store")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)
