import os
from datetime import timedelta

SECRET_KEY = "supersecritkey"
ALGORITHM = "HS256"
TOKEN_EXP = timedelta(days=7)
DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/animegen"
SERVER_URL: str = "http://192.168.18.19:8000"
FILE_STORAGE_PATH: str = os.path.join(os.getcwd(), "image_store")
if not os.path.exists(FILE_STORAGE_PATH):
    os.mkdir(FILE_STORAGE_PATH)