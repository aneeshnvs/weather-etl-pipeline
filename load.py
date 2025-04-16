import pymongo
from config import MONGO_URI, DB_NAME, WEATHER_COLLECTION
from utils import get_logger

logger = get_logger("load")

def delete_weather_data(start_date):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[WEATHER_COLLECTION]
        result = collection.delete_many({"date": start_date})
        logger.info(f"Deleted {result.deleted_count} records for {start_date}")
    except Exception as e:
        logger.error(f"Error deleting weather data: {e}")

def load_weather_data(weather_data_list):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[WEATHER_COLLECTION]
        collection.insert_many(weather_data_list)
        logger.info(f"Inserted {len(weather_data_list)} new records.")
    except Exception as e:
        logger.error(f"Error inserting weather data: {e}")
