# Weather Data Pipeline

A containerized ETL pipeline that extracts hourly temperature data from the Open-Meteo API, stores the extracted data temporarily as CSV, loads it into PostgreSQL, and orchestrates the workflow with Apache Airflow.

## Overview

The project implements a simple weather-data pipeline using:

- **Python** for the ETL logic
- **Open-Meteo API** as the weather-data source
- **Pandas** for data handling
- **SQLAlchemy** for PostgreSQL connectivity
- **PostgreSQL** for weather-data storage
- **Apache Airflow** for workflow orchestration
- **Docker Compose** for the Airflow environment and PostgreSQL storage database
- **Redis** as the Celery broker used by the Airflow setup

The pipeline flow is:

```text
Open-Meteo API
      │
      ▼
   Extract
      │
      ▼
intermediate_data.csv
      │
      ▼
     Load
      │
      ▼
 PostgreSQL
      │
      ▼
   Cleanup
```

## Pipeline Workflow

The Airflow DAG is named:

```text
Weather_pipeline
```

It contains three tasks:

```text
extract_data_from_source
          │
          ▼
load_data_to_destination
          │
          ▼
remove_intermediate_data
```

The task dependency is defined as:

```python
extract_data_task >> load_data_task >> remove_intermediate_data
```

### 1. Extract

The `extract()` function:

1. Generates a random latitude between `-90` and `90`.
2. Generates a random longitude between `-180` and `180`.
3. Sends the coordinates to the Open-Meteo forecast API.
4. Requests hourly `temperature_2m` data.
5. Creates a Pandas DataFrame containing:
   - `latitude`
   - `longitude`
   - `time`
   - `temperature`
6. Saves the DataFrame to:

```text
./intermediate_data.csv
```

### 2. Load

The `load()` function reads:

```text
./intermediate_data.csv
```

and appends its contents to the PostgreSQL table:

```text
weather_data
```

The data is written using Pandas `to_sql()` with SQLAlchemy.

### 3. Cleanup

The `remove_file()` function removes:

```text
./intermediate_data.csv
```

after the loading task.

## Airflow Schedule

The DAG is configured with the following schedule:

```text
* * * * *
```

This schedules the DAG to run every minute.

The DAG start date is:

```text
2026-08-16
```

## Technologies

| Technology | Usage |
|---|---|
| Python | ETL implementation |
| Apache Airflow 3.3.1 | Workflow orchestration |
| Open-Meteo | Weather API |
| Requests | HTTP requests |
| Pandas | DataFrame and CSV processing |
| SQLAlchemy | Database connection |
| PostgreSQL 16 | Airflow database and weather-data storage |
| Redis 7.2 | Celery broker |
| Docker | Containerization |
| Docker Compose | Service orchestration |

## Project Files

```text
.
├── pipeline.py
├── Utilities.py
├── docker-compose-airflow.yaml
├── docker-compose-system.yaml
├── Dockerfile
└── Database_Table_Creation
```

### `pipeline.py`

Contains the Airflow DAG and defines the three pipeline tasks:

```text
extract_data_from_source
load_data_to_destination
remove_intermediate_data
```

### `Utilities.py`

Contains the ETL functions:

```python
extract()
load()
remove_file()
```

It also contains the Open-Meteo API configuration, PostgreSQL connection, logging configuration, and intermediate CSV path.

### `docker-compose-airflow.yaml`

Defines the Airflow environment, including:

- Airflow API server
- Airflow scheduler
- Airflow DAG processor
- Airflow worker
- Airflow triggerer
- Airflow initialization service
- PostgreSQL
- Redis

The Airflow setup uses:

```text
CeleryExecutor
```

and connects the Airflow services to Redis and PostgreSQL.

### `docker-compose-system.yaml`

Defines the PostgreSQL container used for storing the weather data:

```text
postgres_storage
```

The PostgreSQL container port `5432` is exposed on host port `5433`.

### `Dockerfile`

Defines the PostgreSQL image used by the project:

```dockerfile
FROM postgres

EXPOSE 5432

CMD ["postgres"]
```

### `Database_Table_Creation`

Contains the SQL used to create the weather database and table.

## Database

The project creates a database named:

```text
Weather_DB
```

The weather data is stored in:

```text
weather_data
```

### Table Schema

```sql
CREATE TABLE weather_data(
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    time TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL
);
```

The table contains:

| Column | Type | Description |
|---|---|---|
| `id` | `SERIAL` | Primary key |
| `latitude` | `FLOAT` | Latitude returned by Open-Meteo |
| `longitude` | `FLOAT` | Longitude returned by Open-Meteo |
| `time` | `TIMESTAMP` | Weather-data timestamp |
| `temperature` | `FLOAT` | Hourly temperature |

## Database Connection

The ETL code connects to PostgreSQL using SQLAlchemy.

The configured connection is:

```text
postgresql+psycopg2://postgres:admin@postgres_storage:5432/weather_db
```

The Docker service used as the database hostname is:

```text
postgres_storage
```

The storage PostgreSQL service is exposed to the host on:

```text
localhost:5433
```

while PostgreSQL listens on port `5432` inside the container.

## Running the Project

### Prerequisites

The project requires:

- Docker
- Docker Compose

### 1. Start the PostgreSQL Storage Container

Run:

```bash
docker compose -f docker-compose-system.yaml up -d
```

This starts the PostgreSQL container:

```text
postgres_storage
```

### 2. Create the Database

Connect to PostgreSQL:

```bash
docker exec -it postgres_storage psql -U postgres
```

Create the database:

```sql
CREATE DATABASE Weather_DB;
```

Then create the table:

```sql
CREATE TABLE weather_data(
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    time TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL
);
```

### 3. Start Airflow

Start the Airflow environment:

```bash
docker compose -f docker-compose-airflow.yaml up -d
```

The Airflow API server is exposed on:

```text
http://localhost:8080
```

The Airflow Compose configuration creates the default Airflow user with:

```text
Username: airflow
Password: airflow
```

unless these values are overridden through the environment configuration.

### 4. Run the DAG

Open the Airflow interface at:

```text
http://localhost:8080
```

Locate:

```text
Weather_pipeline
```

and run the DAG.

The tasks execute in this order:

```text
extract_data_from_source
        ↓
load_data_to_destination
        ↓
remove_intermediate_data
```

## Checking the Data

After the pipeline has successfully executed, the stored records can be queried with:

```sql
SELECT * FROM weather_data;
```

The project also includes this query in:

```text
Database_Table_Creation
```

## Docker Services

### Airflow Environment

The Airflow Compose configuration contains the following services:

```text
postgres
redis
airflow-apiserver
airflow-scheduler
airflow-dag-processor
airflow-worker
airflow-triggerer
airflow-init
airflow-cli
flower
```

`flower` is configured as an optional Compose profile.

### Weather Storage Database

The separate system Compose file contains:

```text
postgres_storage
```

This container is responsible for the PostgreSQL database used by the weather-data pipeline.

## Configuration

The Airflow Compose configuration reads environment variables from:

```text
.env
```

It supports configuration values including:

```text
AIRFLOW_UID
AIRFLOW_IMAGE_NAME
AIRFLOW_PROJ_DIR
FERNET_KEY
_AIRFLOW_WWW_USER_USERNAME
_AIRFLOW_WWW_USER_PASSWORD
AIRFLOW__API_AUTH__JWT_SECRET
AIRFLOW__API_AUTH__JWT_ISSUER
```

The default Airflow image configured in the Compose file is:

```text
apache/airflow:3.3.1
```

## Logging

The Python ETL code uses Python's logging module.

The configured log format is:

```text
%(levelname)s - %(name)s - %(message)s
```

The extraction, loading, and cleanup functions log the beginning/end of their operations and log exceptions when errors occur.

## Error Handling

The ETL functions use `try/except` blocks.

For extraction and loading, exceptions are logged and raised again.

The cleanup function logs an error if removing the intermediate file fails.

## Data Source

The pipeline uses the Open-Meteo forecast API:

```text
https://api.open-meteo.com/v1/forecast
```

The request currently asks for:

```text
hourly=temperature_2m
```

using randomly generated latitude and longitude coordinates.

## License

The project does not currently contain a separate project license file.

## Author

**Your Name**

Replace this section with your GitHub profile information.

## Project Structure

```text
Weather Data Pipeline
│
├── pipeline.py
│   └── Airflow DAG
│
├── Utilities.py
│   ├── extract()
│   ├── load()
│   └── remove_file()
│
├── docker-compose-airflow.yaml
│   └── Airflow + Redis + PostgreSQL environment
│
├── docker-compose-system.yaml
│   └── PostgreSQL weather-data storage
│
├── Dockerfile
│   └── PostgreSQL image
│
└── Database_Table_Creation
    └── Database and table SQL
```
