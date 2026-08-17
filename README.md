# Weather Data Pipeline 🌦️

An automated ETL pipeline built with **Apache Airflow** that extracts real-time weather data for randomly sampled coordinates, transforms it, and loads it into a **PostgreSQL** database — all orchestrated inside Docker containers.

## Overview

This project periodically:

1. **Extracts** current weather data from the [Open-Meteo](https://open-meteo.com/) API for a randomly generated latitude/longitude, and reverse-geocodes that location (city, state, country) using the [API Ninjas Reverse Geocoding](https://api-ninjas.com/api/reversegeocoding) API.
2. **Transforms** the raw data (e.g. casting `is_day` to a boolean) and writes it to an intermediate CSV.
3. **Loads** the cleaned data into a `weather_data` table in PostgreSQL.
4. **Cleans up** the intermediate/extracted CSV files once the load completes.

The pipeline is defined as an Airflow DAG (`Weather_pipeline`) that runs on a `* * * * *` (every minute) schedule and is fully containerized with Docker Compose.

## Architecture

```
                ┌────────────────────┐
                │   Open-Meteo API   │
                └─────────┬──────────┘
                          │
┌───────────────────┐     │    ┌─────────────────────────┐
│  API Ninjas       │ ◄───┼───►│  Airflow DAG            │
│ (Reverse Geocode) │     │    │   extract → transform → │
└───────────────────┘     │    │  load → remove_file     │
                          │    └────────────┬────────────┘
                          │                 │
                          ▼                 ▼
                  extracted_data.csv   PostgreSQL
                  intermediate_data.csv (weather_data table)
```

<!-- Replace the image path below with your architecture diagram, e.g. docs/images/architecture.png -->
![Architecture Diagram](docs/images/architecture.png)

**Services:**

| Service | Purpose |
|---|---|
| `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init` | Apache Airflow (CeleryExecutor) components that orchestrate and run the DAG |
| `postgres` | Airflow's own metadata database |
| `redis` | Celery broker for distributing tasks to workers |
| `postgres_storage` | Dedicated PostgreSQL instance that stores the extracted weather data |
| `flower` *(optional)* | Celery monitoring UI |

## Project Structure

```
.
├── Dockerfile                      # Builds the weather-data Postgres image
├── docker-compose-airflow.yaml     # Airflow cluster (scheduler, workers, webserver, etc.)
├── docker-compose-system.yaml      # Dedicated Postgres instance for storing weather data
├── Database_Table_Creation         # SQL to create the database and weather_data table
├── dags/
│   └── pipeline.py                 # Airflow DAG definition
├── Utilities.py                    # Extract / transform / load / cleanup logic
└── docs/
    └── images/                     # Architecture diagram, DAG graph screenshots, etc.
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- At least 4 GB RAM and 2 CPUs available to Docker (Airflow's recommended minimum)
- An [API Ninjas](https://api-ninjas.com/) API key (for reverse geocoding)

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Set up environment variables

Airflow requires an `.env` file (or exported variables) alongside `docker-compose-airflow.yaml`:

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

You'll also need a Fernet key for Airflow:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add it to your `.env`:

```
FERNET_KEY=<generated-key>
```

> ⚠️ **Security note:** `Utilities.py` currently contains a hardcoded API Ninjas key. Before running this yourself, replace it with an environment variable (e.g. `os.environ["API_NINJAS_KEY"]`) and pass it in via `.env` / Docker secrets rather than committing it to source control.

### 3. Create the weather storage database

Start the storage Postgres container:

```bash
docker compose -f docker-compose-system.yaml up -d
```

Then run the DDL script against it to create the database and table:

```bash
docker exec -i postgres_storage psql -U postgres < Database_Table_Creation
```

### 4. Start Airflow

```bash
docker compose -f docker-compose-airflow.yaml up airflow-init
docker compose -f docker-compose-airflow.yaml up -d
```

### 5. Access the Airflow UI

Open [http://localhost:8080](http://localhost:8080) and log in with the default credentials:

- **Username:** `airflow`
- **Password:** `airflow`

Unpause the `Weather_pipeline` DAG to begin execution.

## DAG Details

The `Weather_pipeline` DAG (`dags/pipeline.py`) runs every minute and consists of four sequential tasks:

| Task | Function | Description |
|---|---|---|
| `extract_data_from_source` | `extract()` | Picks a random lat/long, reverse-geocodes it, fetches current weather from Open-Meteo, saves to `extracted_data.csv` |
| `transform_data` | `transform()` | Casts `is_day` to boolean, writes `intermediate_data.csv` |
| `load_data_to_destination` | `load()` | Appends the transformed data into the `weather_data` Postgres table |
| `remove_intermediate_data` | `remove_file()` | Deletes the CSV artifacts generated during the run |

```
extract_data_from_source >> transform_data >> load_data_to_destination >> remove_intermediate_data
```

<!-- Replace the image path below with a screenshot of the DAG graph from the Airflow UI, e.g. docs/images/dag_graph.png -->
![DAG Graph](docs/images/dag_graph.png)

## Database Schema

The `weather_data` table (see `Database_Table_Creation`) stores, for each run:

- Location metadata: `name`, `country`, `state`, `latitude`, `longitude`, `timezone`, `elevation`
- Current weather readings: `temperature_2m`, `relative_humidity_2m`, `precipitation`, `rain`, `showers`, `snowfall`, `pressure_msl`, `surface_pressure`, `cloud_cover`, `weather_code`, `wind_speed_10m`, `wind_direction_10m`, `wind_gusts_10m`, `apparent_temperature`
- Metadata: `is_day`, `time`, `interval`, `generationtime_ms`, `utc_offset_seconds`

## Tech Stack

- **Orchestration:** Apache Airflow 3.3.1 (CeleryExecutor)
- **Message Broker:** Redis
- **Databases:** PostgreSQL (Airflow metadata + weather data storage)
- **Language:** Python (pandas, SQLAlchemy, requests)
- **Containerization:** Docker & Docker Compose
- **APIs:** Open-Meteo, API Ninjas

## Notes & Future Improvements

- Coordinates are currently randomized on every run for demonstration purposes; this could be replaced with a fixed list of cities of interest.
- Secrets (API keys, database passwords) should be moved out of source code and into environment variables or a secrets manager.
- Add retries/backoff around the external API calls in `extract()` for resilience against transient failures.
- Add data quality checks (e.g. with Great Expectations) between the transform and load steps.

## License

This project uses Apache Airflow, which is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0). Add your own license here for the rest of the project.
