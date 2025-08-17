# bot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

THE_DOG_API_KEY = os.getenv("THE_DOG_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not THE_DOG_API_KEY:
    raise RuntimeError("THE_DOG_API_KEY not set in .env")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in .env")