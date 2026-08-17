import os
import requests as r
import pandas as pd
import sqlalchemy as sql
import logging as l
import random


meteo_url = "https://api.open-meteo.com/v1/forecast"

logger = l.getLogger(__name__)
l.basicConfig(format = '%(levelname)s - %(name)s - %(message)s' , level = l.DEBUG)
database_url = "postgresql+psycopg2://postgres:admin@postgres_storage:5432/weather_db"
engine = sql.create_engine(database_url)
con = engine.connect()
table = 'weather_data'
extracted_data_path = "./extracted_data.csv"
intermediate_data_path = "./intermediate_data.csv"

def extract():
    try: 
        latitude = random.randint(-90 , 90)
        longitude = random.randint(-180 , 180)

        logger.info("Extraction of data from API starts...")

        meteo_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "rain", "showers", "snowfall", "pressure_msl", "surface_pressure", "cloud_cover", "weather_code", "wind_gusts_10m", "wind_direction_10m", "wind_speed_10m", "apparent_temperature"],
        }

        
        meteo_results = dict(r.get(meteo_url , params = meteo_params).json())
        meteo_results.pop('current_units')
        meteo_results_df = pd.json_normalize(meteo_results)
        meteo_results_df.columns = list(map(lambda column: column.replace('current.' , '') , list(meteo_results_df.columns)))

        meteo_results_df.to_csv(extracted_data_path, index = False)
        
        logger.info("Extraction of data from API Ends.")

        return extracted_data_path
    except Exception as e:
        l.error(f"Error in extraction of data ({e})")
        raise Exception

def transform():
    try:
        logger.info("Transforamtion of data starts...")
        results = pd.read_csv(extracted_data_path)

        results.is_day = results.is_day.astype(dtype = 'boolean')

        results.to_csv(intermediate_data_path , index = False)
        logger.info("Transforamtion of data ends...")
    except Exception as e:
        l.error(f"Error in transforamtion of data ({e})")
        raise Exception



def load():
    try:
        results = pd.read_csv(intermediate_data_path)

        logger.info("Loading of data starts...")

        results.to_sql(table , con , if_exists='append' , index = False)

        logger.info("Loading of data ends.") 
    except Exception as e:
        l.error(f"Error in loading of data ({e})")
        raise Exception

def remove_file():
    try:
        os.remove(intermediate_data_path)
        os.remove(extracted_data_path)
        logger.info(f"intermediate data file has been removed from {intermediate_data_path}")
    except Exception as e:
        logger.error(f"Error in removing intermediate data file: {e}")



