from extract import get_all_cities, read_weather_data
from transform import process_weather_data
from load import delete_weather_data, load_weather_data
from checkpoint import update_pipeline
from utils import get_logger

logger = get_logger("main")

def main():
    start_date = "2025-03-26"
    end_date = "2025-03-26"

    try:
        logger.info("Starting weather ETL pipeline")
        all_cities = get_all_cities()
        weather_data_list = []

        for city in all_cities:
            raw_data = read_weather_data(city, start_date, end_date)
            if raw_data:
                processed = process_weather_data(city['name'], start_date, raw_data)
                weather_data_list.append(processed)

        delete_weather_data(start_date)
        load_weather_data(weather_data_list)
        update_pipeline(weather_data_list, start_date)

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == '__main__':
    main()
