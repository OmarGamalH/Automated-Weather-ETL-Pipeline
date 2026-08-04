# 🌦️ Weather Data Engineering Pipeline

An end-to-end data engineering project that collects weather data from a public API, cleans and transforms the raw data, stores it in PostgreSQL, and makes it available for analysis and visualization.

The project demonstrates a practical **ETL (Extract, Transform, Load)** workflow using **Python, PostgreSQL, Apache Airflow, Docker, and SQL**.

---

## 📌 Project Overview

Weather information is continuously generated through APIs, but raw API responses are not always directly suitable for analysis. They may contain unnecessary fields, inconsistent formats, missing values, and timestamps that require processing.

The goal of this project is to build an automated pipeline that:

1. Extracts weather data from a weather API.
2. Cleans and transforms the raw data.
3. Validates the processed information.
4. Stores the data in PostgreSQL.
5. Runs automatically at scheduled intervals.
6. Makes historical weather data available for analysis and visualization.

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────┐
                    │   Weather API   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Python      │
                    │     Extract     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Transform &     │
                    │ Data Cleaning   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Data Validation │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SQL / Dashboard │
                    │    Analysis     │
                    └─────────────────┘

                 Apache Airflow
             orchestrates the workflow

                      Docker
              provides the environment
```

---

## 🎯 Project Objectives

* Build a real-world ETL pipeline.
* Retrieve data from an external REST API.
* Process and clean raw JSON data.
* Store structured data in PostgreSQL.
* Automate the pipeline with Apache Airflow.
* Containerize the project with Docker.
* Implement basic data-quality checks.
* Analyze historical weather information using SQL.
* Prepare data for visualization in Power BI or Tableau.

---

## 📥 Data Collection

The pipeline retrieves weather information for selected cities.

Depending on the weather API used, the dataset can include:

| Field               | Description                         |
| ------------------- | ----------------------------------- |
| `city`              | Name of the city                    |
| `country`           | Country name/code                   |
| `latitude`          | Geographic latitude                 |
| `longitude`         | Geographic longitude                |
| `observation_time`  | Time of the weather observation     |
| `temperature`       | Current temperature                 |
| `feels_like`        | Feels-like temperature              |
| `humidity`          | Relative humidity                   |
| `pressure`          | Atmospheric pressure                |
| `wind_speed`        | Wind speed                          |
| `weather_condition` | Current weather condition           |
| `precipitation`     | Precipitation amount                |
| `ingested_at`       | Time the pipeline stored the record |

Example record:

```text
City: Cairo
Temperature: 31.5°C
Humidity: 62%
Wind Speed: 18 km/h
Pressure: 1008 hPa
Condition: Clear
Timestamp: 2026-08-04 05:00:00
```

---

## 🔄 ETL Pipeline

### 1. Extract

Python sends HTTP requests to the weather API and retrieves the latest weather information.

The extraction process handles:

* API requests
* API authentication where required
* Response parsing
* Connection errors
* API errors
* Request timeouts
* Invalid responses

The response is initially treated as raw data.

### 2. Transform

The raw API response is cleaned and converted into a consistent format.

Transformation tasks include:

* Selecting required fields.
* Converting temperature units.
* Standardizing city names.
* Converting timestamps.
* Handling missing values.
* Removing duplicate records.
* Validating numerical values.
* Adding an ingestion timestamp.
* Converting API data into a database-friendly structure.

### 3. Load

The transformed data is loaded into PostgreSQL.

The database stores historical weather records so that weather patterns can be analyzed over time.

---

## 🗄️ PostgreSQL Database

A possible database table is:

```text
weather_data
--------------------------------
id
city
country
latitude
longitude
observation_time
temperature
feels_like
humidity
pressure
wind_speed
weather_condition
precipitation
ingested_at
```

Example SQL query:

```sql
SELECT
    city,
    AVG(temperature) AS average_temperature
FROM weather_data
GROUP BY city
ORDER BY average_temperature DESC;
```

---

## ✅ Data Quality

Data-quality checks are included to prevent invalid information from entering the database.

The pipeline can validate that:

* `city` is not NULL.
* `temperature` is within a reasonable range.
* `humidity` is between 0 and 100.
* `wind_speed` is not negative.
* `observation_time` is valid.
* Duplicate records are not inserted.
* Required API fields are present.

If invalid data is detected, the pipeline can log the issue and prevent the bad record from being loaded.

---

## ⏰ Workflow Orchestration

Apache Airflow is used to automate and orchestrate the pipeline.

A typical DAG can contain:

```text
start
  ↓
extract_weather_data
  ↓
validate_response
  ↓
transform_weather_data
  ↓
validate_data
  ↓
load_to_postgresql
  ↓
finish
```

The pipeline can be scheduled to run hourly.

```text
08:00 → Extract → Transform → Load
09:00 → Extract → Transform → Load
10:00 → Extract → Transform → Load
11:00 → Extract → Transform → Load
```

This allows the system to continuously build a historical weather dataset without manual execution.

---

## 🐳 Docker

Docker can be used to containerize the project's services.

Possible containers include:

* Python application
* PostgreSQL
* Apache Airflow
* Supporting services

Using Docker makes the project easier to run consistently across different environments.

---

## 📊 Data Analysis

Once enough historical data has been collected, SQL can be used to analyze the dataset.

### Average temperature by city

```sql
SELECT
    city,
    AVG(temperature) AS average_temperature
FROM weather_data
GROUP BY city;
```

### Maximum temperature

```sql
SELECT
    MAX(temperature) AS maximum_temperature
FROM weather_data;
```

### Average humidity by city

```sql
SELECT
    city,
    AVG(humidity) AS average_humidity
FROM weather_data
GROUP BY city;
```

### Other possible analyses

* Hottest and coldest days.
* Average temperature by city.
* Average humidity.
* Maximum wind speed.
* Rainfall trends.
* Temperature by hour.
* Temperature changes over time.
* Weather comparison between cities.

---

## 📈 Dashboard

The processed data can be connected to a visualization platform such as **Power BI** or **Tableau**.

A dashboard could display:

* Current temperature.
* Average temperature.
* Humidity.
* Wind speed.
* Rainfall.
* Temperature trends.
* City comparisons.
* Historical weather patterns.

---

## 🛠️ Technology Stack

| Component        | Technology         |
| ---------------- | ------------------ |
| Programming      | Python             |
| Data Source      | Weather API        |
| Data Processing  | Pandas / Python    |
| Database         | PostgreSQL         |
| Orchestration    | Apache Airflow     |
| Containerization | Docker             |
| Query Language   | SQL                |
| Visualization    | Power BI / Tableau |
| Version Control  | Git / GitHub       |

---

## 📁 Suggested Project Structure

```text
weather-data-engineering/
│
├── dags/
│   └── weather_pipeline.py
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── config.py
│
├── sql/
│   ├── create_tables.sql
│   └── analysis.sql
│
├── tests/
│   └── test_pipeline.py
│
├── data/
│   └── sample/
│
├── logs/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

Make sure the following are installed:

* Python 3.10+
* Docker
* Docker Compose
* Git
* PostgreSQL (optional if running it through Docker)

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd weather-data-engineering
```

### 2. Create an environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Add your API key and database configuration to `.env`.

Example:

```env
WEATHER_API_KEY=your_api_key
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=weather_db
POSTGRES_USER=weather_user
POSTGRES_PASSWORD=your_password
```

> Never commit `.env` or API keys to GitHub.

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Docker environment

```bash
docker compose up -d
```

### 5. Check running containers

```bash
docker compose ps
```

### 6. Stop the environment

```bash
docker compose down
```

---

## 🔐 Environment Variables

Create a `.env` file containing the required configuration.

```env
WEATHER_API_KEY=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Keep secrets out of source control.

---

## 🚀 Pipeline Execution

The pipeline can be executed manually during development or automatically through Airflow.

Typical workflow:

```text
1. Airflow starts the DAG
2. Python requests weather data
3. Raw API response is received
4. Data is transformed
5. Data-quality checks are executed
6. Valid records are loaded into PostgreSQL
7. Logs are generated
8. Pipeline completes
```

---

## 📌 Expected Outcome

The final system is an automated end-to-end weather data platform capable of:

* Collecting weather data at regular intervals.
* Processing raw API responses.
* Validating data quality.
* Storing historical weather data.
* Automating workflows.
* Querying data using SQL.
* Supporting analytical dashboards.

The project demonstrates practical knowledge of:

* Data ingestion
* ETL pipelines
* Data transformation
* SQL
* PostgreSQL
* Workflow orchestration
* Automation
* Data quality
* Docker
* Data analysis

---

## 🔮 Future Improvements

The project can be extended with:

* AWS S3 or another cloud object store.
* Cloud data warehouses such as Snowflake or BigQuery.
* Apache Spark for large-scale processing.
* Apache Kafka for real-time streaming.
* dbt for analytics transformations.
* Automated data-quality testing.
* CI/CD using GitHub Actions.
* Pipeline monitoring and alerting.
* Real-time weather dashboards.
* Support for hundreds or thousands of cities.
* Separate raw, cleaned, and analytics layers.

---

## 💼 Skills Demonstrated

This project demonstrates the following data engineering skills:

```text
Python
   ↓
REST APIs
   ↓
ETL / ELT
   ↓
Data Cleaning
   ↓
SQL
   ↓
PostgreSQL
   ↓
Apache Airflow
   ↓
Docker
   ↓
Data Quality
   ↓
Data Visualization
```

---

## 📝 Project Summary

**The Weather Data Engineering Pipeline is an automated ETL system that collects weather data from an external API, performs data cleaning and transformation using Python, validates the processed information, and stores historical weather records in PostgreSQL. Apache Airflow is used to schedule and orchestrate the workflow, while Docker provides a consistent environment for running the system. The resulting dataset can be queried using SQL and connected to a BI dashboard for analysis.**

This project demonstrates the complete data engineering lifecycle, from **data ingestion and transformation to storage, orchestration, quality validation, and visualization**.

---

## 👨‍💻 Author

**Your Name**

* GitHub: `<your-github-profile>`
* LinkedIn: `<your-linkedin-profile>`

---

## 📄 License

This project is intended for educational and portfolio purposes. Add a license here if you plan to distribute the project publicly.
