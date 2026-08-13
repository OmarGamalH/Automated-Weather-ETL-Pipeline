import os
import requests as r
import pandas as pd
import sqlalchemy as sql


api_url = "https://api.open-meteo.com/v1/forecast"
latitude = 52.52 
longitude = 13.41
database_url = "postgresql+psycopg2://postgres:admin@postgres_container:5432/weather_db"
engine = sql.create_engine(database_url)

con = engine.connect()


def extract(api_url , latitude , longitude):
    params = {'latitude' : latitude , 'longitude' : longitude , 'hourly' : 'temperature_2m'}
    results = r.get(api_url , params = params).json()
    results_formated = {'latitude' : results['latitude'] , 'longitude' : results['longitude'] , 'time' : results['hourly']['time'] , 'temperature' : results['hourly']['temperature_2m']}
    results_df = pd.DataFrame(results_formated)
    return results_df


def load(results , table , con):
    results.to_sql(table , con , if_exists='append' , index = False) 


def main():
    results = extract(api_url , latitude = latitude , longitude = longitude)
    load(results , 'weather_data' , con)

if __name__ == "__main__":
    main()

