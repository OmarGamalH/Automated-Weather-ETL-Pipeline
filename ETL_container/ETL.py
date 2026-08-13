import os
import requests as r
import pandas as pd
import sqlalchemy as sql
import logging as l


api_url = "https://api.open-meteo.com/v1/forecast"
latitude = 52.52 
longitude = 13.41

logger = l.getLogger(__name__)
current_dir = os.getcwd()
l.basicConfig( filename = os.path.join(current_dir , "logs/logs.log") , format = '%(levelname)s - %(name)s - %(message)s' , level = l.DEBUG)



database_url =  "postgresql+psycopg2://postgres:admin@postgres_container:5432/weather_db"
engine = sql.create_engine(database_url)

con = engine.connect()


def extract(api_url , latitude , longitude):
    try: 
        logger.info("Extraction of data from API starts...")
        params = {'latitude' : latitude , 'longitude' : longitude , 'hourly' : 'temperature_2m'}
        results = r.get(api_url , params = params).json()
        results_formated = {'latitude' : results['latitude'] , 'longitude' : results['longitude'] , 'time' : results['hourly']['time'] , 'temperature' : results['hourly']['temperature_2m']}
        results_df = pd.DataFrame(results_formated)
        logger.info("Extraction of data from API Ends.")
        return results_df
    except Exception as e:
        l.error(f"Error in extraction of data ({e})")
        return None


def load(results , table , con):
    try:
        logger.info("Loading of data starts...")
        results.to_sql(table , con , if_exists='append' , index = False)
        logger.info("Loading of data ends.") 
    except Exception as e:
        l.error(f"Error in loading of data ({e})")
        return None

def main():
    results = extract(api_url , latitude = latitude , longitude = longitude)
    load(results , 'weather_data' , con)

if __name__ == "__main__":
    main()

