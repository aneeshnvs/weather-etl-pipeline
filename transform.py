from utils import get_logger

logger = get_logger("transform")

def process_weather_data(city_name, date, weather_data):
    logger.info(f"Processing weather data for city: {city_name} on date: {date}")
    document = {
        "city": city_name,
        "date": date,
        "data": []
    }

    try:
        for i, time_string in enumerate(weather_data['hourly']['time']):
            hour = int(time_string.split('T')[1].split(':')[0])
            document['data'].append({
                "hour": hour,
                "temperature": weather_data['hourly']['temperature_2m'][i],
                "precipitation": weather_data['hourly']['precipitation_probability'][i],
                "rain": weather_data['hourly']['rain'][i]
            })
    except Exception as e:
        logger.error(f"Error processing data for {city_name}: {e}")

    return document
