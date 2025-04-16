# Weather ETL Pipeline – Project Overview



---

1. `main.py`
This is the **entry point** of the project.  
It runs the entire ETL process — Extracts weather data, Transforms it, Loads it into MongoDB, and updates a checkpoint.

How to run it:
```bash
python main.py
```

---

 2. `extract.py`
Talks to two things:
- Your **MongoDB database** to get city coordinates
- The **Open-Meteo API** to fetch hourly weather data for those cities

Functions:
- `get_all_cities()`: Gets a list of all cities and their coordinates from MongoDB  
- `read_weather_data(city, start_date, end_date)`: Calls the weather API for each city

---

3. `transform.py`
Cleans and structures the data returned from the API

Function:
- `process_weather_data(city_name, date, weather_data)`: 
  - Takes raw API data
  - Formats it to include: hour, temperature, rain, precipitation

---

4. `load.py`
 This file inserts the cleaned weather data into MongoDB  
Also deletes any old records for the same date (to prevent duplicates)

Functions:
- `delete_weather_data(start_date)`: Removes old data for the same date  
- `load_weather_data(weather_data_list)`: Inserts new weather records

---

5. `checkpoint.py`
Tracks the last successful ETL run so you don’t reprocess the same day twice

Function:
- `update_pipeline(weather_data_list, start_date)`: 
  - Updates a checkpoint collection in MongoDB with date, status, and city info

---

6. `config.py`


Contains variables:
```python
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "weather_db"
CITY_COLLECTION = "city_coordinates"
WEATHER_COLLECTION = "city_weather_hourly"
CHECKPOINT_COLLECTION = "pipeline_checkpoint"
```

---

7. `utils.py`
📋 Adds logging so you can see what’s happening when you run the code

Function:
- `get_logger(name)`: Creates a logger with timestamps and error levels

---

How to Run the Project (Start to Finish)

---

1. Clone or download the project folder

```bash
cd /Users/aneesh/weather-pipeline
```

---

2. Activate your virtual environment

```bash
source wp-venv/bin/activate
```

---

3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, generate it with:
```bash
./wp-venv/bin/python3 -m pip freeze > requirements.txt
```

---

4. Make sure MongoDB is running locally

- You should have MongoDB installed and running
- It should have a database called `weather_db`
- Inside it, a collection named `city_coordinates` with city names and their coordinates

Example document:
```json
{
  "name": "London",
  "latitude": 51.5074,
  "longitude": -0.1278
}
```

---

5. Run the ETL Pipeline

bash
python main.py


This will:
1. Fetch city list from MongoDB
2. Call the Open-Meteo API for each city
3. Clean and prepare the weather data
4. Delete old weather records for the same date
5. Insert new records into MongoDB
6. Log the entire process
7. Save the pipeline status into a checkpoint