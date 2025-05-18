# settings.py
import os
from dotenv import load_dotenv

load_dotenv()
# this method reads the .env file
# and assigns the environment variables their values

USERNAME = os.getenv("email", "abc@gmail.com")
PASSWORD = os.getenv("password", "")
API_KEY = os.getenv("api_key", "")
LOOKBACK_PERIOD_DAYS = os.getenv("lookback_period_days","365")
TECHNICAL_INDICATORS = os.getenv("technical_indicators","")
UPDATE_FREQUENCY_HOURS = os.getenv("update_frequency_hours","")
IS_DEBUG = os.getenv("is_debug","")
MODEL = os.getenv("model","gpt-4o")