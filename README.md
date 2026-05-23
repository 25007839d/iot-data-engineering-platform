# IoT Data Engineering Platform Documentation

## Project Overview

This project is designed to build a complete IoT-based modern data engineering platform using:

- Sensors
- Arduino / ESP32
- Render Flask API
- Google Forms & Google Sheets
- Supabase PostgreSQL

The platform supports:
- Real-time IoT data ingestion
- Batch master data onboarding
- Cloud ETL processing
- BigQuery analytics
- Dashboarding
- AI/ML future integration

---

# 1. Sensors Layer

## Purpose

Sensors collect machine/environment data in real time.

---

## Sensors Used

| Sensor | Purpose |
|---|---|
| DHT11 / DHT22 | Temperature & Humidity |
| SW-420 | Vibration Detection |
| ACS712 | Current Monitoring |

---

## Data Generated

Example:

```json
{
  "temperature": 35,
  "vibration": 1,
  "current": 2.5
}
```

---

# 2. Arduino / ESP32 Layer

## Purpose

ESP32 acts as the IoT edge device.

Responsibilities:
- Read sensor values
- Connect to WiFi
- Send HTTP POST requests
- Push real-time data to API

---

## Hardware Components

| Component | Purpose |
|---|---|
| ESP32 | Main Controller |
| Breadboard | Connections |
| Jumper Wires | Wiring |
| DHT11 | Temperature |
| SW-420 | Vibration |
| ACS712 | Current Sensor |

---

## Data Flow

```text
Sensors
   ↓
ESP32
   ↓
WiFi
   ↓
Flask API
```

---

## Example ESP32 Payload

```json
{
  "machine_id": "M101",
  "temperature": 35,
  "vibration": 1,
  "current": 2.5
}
```

---

# 3. Render Flask API Layer

## Purpose

Render hosts the Flask API.

Responsibilities:
- Receive IoT sensor data
- Validate requests
- Insert records into database
- Expose dashboard endpoints

---

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/sensor` | Receive IoT Data |
| `/dashboard` | Show Live Dashboard |


---

## Technologies Used

| Technology | Purpose |
|---|---|
| Flask | Python Web Framework |
| Gunicorn | Production Server |
| Render | Cloud Hosting |

---

## Example Flask API Flow

```text
ESP32
   ↓
POST /sensor
   ↓
Flask API
   ↓
Supabase PostgreSQL
```

---

# 4. Google Form Layer

## Purpose

Google Form is used for machine onboarding.

Business users can add:
- Machine details
- Plant details
- Machine type
- Installation information

---

## Form Fields

| Field |
|---|
| machine_id |
| machine_name |
| location |
| machine_type |
| install_date |

---

## Flow

```text
Business User
   ↓
Google Form
   ↓
Google Sheet
```

---

# 5. Google Sheet Layer

## Purpose

Acts as raw batch master data source.

Stores:
- Machine master data
- Business onboarding data

---

## Why Google Sheets?

Advantages:
- Easy for business users
- No coding required
- Automatic data storage
- CSV export support

---

## Example Sheet Data

| machine_id | machine_name | location |
|---|---|---|
| M101 | Motor A | Plant 1 |

---

## CSV Export

Google Sheets can export CSV files for ETL processing.

Example:

```text
Google Sheet
   ↓
CSV Export
   ↓
Airflow ETL
```

---

# 6. Supabase PostgreSQL Layer

## Purpose

Supabase acts as the cloud relational database.

Stores:
- sensor_data
- machine_master
- processed analytics tables

---

## Why Supabase?

Advantages:
- Managed PostgreSQL
- Cloud-native
- Free tier available
- Remote access support
- Easy integration with Flask

---

## Example Tables

### sensor_data

| Column | Type |
|---|---|
| id | BIGSERIAL |
| machine_id | TEXT |
| temperature | FLOAT |
| vibration | INT |
| current_value | FLOAT |
| created_at | TIMESTAMP |

---

### machine_master

| Column | Type |
|---|---|
| machine_id | TEXT |
| machine_name | TEXT |
| location | TEXT |
| machine_type | TEXT |

---

# 7. Data Join Logic

## Join Column

```sql
machine_id
```

---

## Example SQL Join

```sql
SELECT

s.machine_id,
s.temperature,
s.vibration,
m.machine_name,
m.location

FROM sensor_data s

JOIN machine_master m

ON s.machine_id = m.machine_id;
```

---

# 8. Final Hybrid Architecture

```text
                STREAMING PIPELINE

Sensors
   ↓
ESP32
   ↓
Render Flask API
   ↓
Supabase sensor_data


                BATCH PIPELINE

Google Form
   ↓
Google Sheet
   ↓
CSV Export
   ↓
ETL Processing
   ↓
Supabase machine_master


                ANALYTICS

sensor_data
      +
machine_master
      ↓
SQL JOIN
      ↓
Dashboard / AI / Reporting
```

---

# 9. Future GCP Expansion

Future integrations:

| Service | Purpose |
|---|---|
| Airflow / Composer | Orchestration |
| Pub/Sub | Streaming |
| Dataflow | ETL Processing |
| Dataproc | Spark Processing |
| BigQuery | Data Warehouse |
| Looker | Dashboards |
| Vertex AI | AI/ML |

---

# 10. Project Benefits

## Technical Benefits

- Real-time IoT ingestion
- Batch + Streaming architecture
- Cloud-native design
- Data warehouse ready
- AI-ready pipeline

---

## Resume Benefits

This project demonstrates:
- IoT Engineering
- Data Engineering
- Cloud Engineering
- ETL Pipelines
- API Development
- PostgreSQL
- Streaming Architecture
- Batch Processing
- GCP Architecture

---

# 11. Final Enterprise Architecture

```text
ESP32 Sensors
        ↓
Render Flask API
        ↓
Supabase PostgreSQL
        ↓
Batch + Streaming Processing
        ↓
BigQuery
        ↓
Looker Dashboards
        ↓
AI / Predictive Maintenance
```

End-to-End Modern Data Engineering & IoT Platform 

