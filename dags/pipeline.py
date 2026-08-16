from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from datetime import datetime
from Utilities import extract , load , remove_file



with DAG("Weather_pipeline" , start_date = datetime(2026, 8, 16) , schedule = "* * * * *"):

    extract_data_task = PythonOperator(task_id = "extract_data_from_source" , python_callable= extract)

    load_data_task = PythonOperator(task_id = "load_data_to_destination" , python_callable= load)

    remove_intermediate_data = PythonOperator(task_id = "remove_intermediate_data" , python_callable= remove_file)

    extract_data_task >> load_data_task >> remove_intermediate_data