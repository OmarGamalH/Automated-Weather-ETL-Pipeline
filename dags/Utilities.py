import os
import requests as r
import pandas as pd
import sqlalchemy as sql
import logging as l
import random

api_url = "https://api.open-meteo.com/v1/forecast"
logger = l.getLogger(__name__)
l.basicConfig(format = '%(levelname)s - %(name)s - %(message)s' , level = l.DEBUG)
database_url = "postgresql+psycopg2://postgres:admin@postgres_storage:5432/weather_db"
engine = sql.create_engine(database_url)
con = engine.connect()
table = 'weather_data'
intermediate_data_path = "./intermediate_data.csv"



def extract():
    try: 
        latitude = random.randint(-90 , 90)
        longitude = random.randint(-180 , 180)

        logger.info("Extraction of data from API starts...")

        params = {'latitude' : latitude , 'longitude' : longitude , 'hourly' : 'temperature_2m'}
        results = r.get(api_url , params = params).json()

        results_formated = {'latitude' : results['latitude'] , 'longitude' : results['longitude'] , 'time' : results['hourly']['time'] , 'temperature' : results['hourly']['temperature_2m']}
        results_df = pd.DataFrame(results_formated)

        logger.info("Extraction of data from API Ends.")

        results_df.to_csv(intermediate_data_path , index = False)
        return intermediate_data_path
    except Exception as e:
        l.error(f"Error in extraction of data ({e})")
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
        logger.info(f"intermediate data file has been removed from {intermediate_data_path}")
    except Exception as e:
        logger.error(f"Error in removing intermediate data file: {e}")




