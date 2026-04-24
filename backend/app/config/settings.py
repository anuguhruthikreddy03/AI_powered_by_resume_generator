import os
from dotenv import load_dotenv
from pathlib import Path

# Get root directory (backend folder)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env explicitly
load_dotenv(dotenv_path=BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in .env file")

SECRET_KEY = os.getenv("SECRET_KEY")