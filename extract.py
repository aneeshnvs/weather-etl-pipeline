import pymongo
import requests
from config import MONGO_URI, DB_NAME, CITY_COLLECTION
from utils import get_logger

logger = get_logger("extract")

def get_all_cities():
    try:
        logger.info("Fetching city coordinates from DB...")
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[CITY_COLLECTION]
        return list(collection.find())
    except Exception as e:
        logger.error(f"Error fetching cities: {e}")
        return []

def read_weather_data(city, start_date, end_date):
    logger.info(f"Reading weather data for city: {city['name']}")
    params = {
        "latitude": city['latitude'],
        "longitude": city['longitude'],
        "hourly": ["temperature_2m", "precipitation_probability", "rain"],
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Request failed for {city['name']}: {e}")
        return None
