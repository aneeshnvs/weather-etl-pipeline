import pymongo
from datetime import datetime, timedelta
from config import MONGO_URI, DB_NAME, CHECKPOINT_COLLECTION
from utils import get_logger

logger = get_logger("checkpoint")

def update_pipeline(weather_data_list, start_date):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[CHECKPOINT_COLLECTION]

        result = collection.find_one({"pipeline_name": "weather_data_ingestion"})

        if result:
            logger.info("Updating existing checkpoint entry...")
            collection.update_one(
                {"pipeline_name": "weather_data_ingestion"},
                {"$set": {
                    "last_processed_date": start_date,
                    "last_run": start_date,
                    "status": "completed",
                    "last_processed_city": weather_data_list[-1]['city'],
                    "nextrun": f"{start_date}T00:00:00Z",
                    "comments": "Processing updated successfully"
                }}
            )
        else:
            logger.info("Inserting new checkpoint entry...")
            collection.insert_one({
                "pipeline_name": "weather_data_ingestion",
                "last_processed_city": weather_data_list[-1]['city'],
                "last_processed_date": start_date,
                "last_run": start_date,
                "status": "completed",
                "nextrun": f"{start_date}T00:00:00Z",
                "comments": "Processing completed successfully"
            })
    except Exception as e:
        logger.error(f"Error updating checkpoint: {e}")
