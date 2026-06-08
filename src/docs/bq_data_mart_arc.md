[//]: # (BQ strecture)

Build an end-to-end Industrial IoT Data Platform to ingest machine sensor data from IoT devices, process data using PySpark, store curated datasets in BigQuery, and prepare data for:

Operational Dashboards
Email Alerting
Machine Learning
2. Source Systems
Source 1: Sensor Data (Supabase PostgreSQL)

Table Name:

sensor_data_v1

Schema:

Column Name	Data Type	Description
id	BIGINT	Unique record identifier
machine_id	STRING	Machine Identifier
temperature	FLOAT	Temperature reading
object_detected_flag	BOOLEAN	Object detected by sensor
buzzer_active_flag	BOOLEAN	Buzzer status
created_at	TIMESTAMP	Event timestamp

Purpose:

Real-time machine monitoring
Sensor event collection
Source 2: Machine Master Data (CSV)

File Name:

machine_master.csv

Schema:

Column Name	Data Type	Description
machine_id	STRING	Machine Identifier
machine_name	STRING	Machine Name
location	STRING	Plant/Location
machine_type	STRING	Machine Category
install_date	DATE	Installation Date
installation_engineer_name	STRING	Installation Engineer
machine_owner_name	STRING	Business Owner

Purpose:

Machine metadata
Ownership information
Machine classification
3. Data Architecture
Supabase
   |
   v
bronze_sensor_data
   |
   v
silver_sensor_data
   |
   +-------------------+
                       |
                       |
                       v

CSV
   |
   v
bronze_machine_master
   |
   v
silver_machine_master
   |
   +-------------------+
                       |
                       |
                       v

               GOLD LAYER

       +----------------------+
       | mart_machine_daily_kpi|
       +----------------------+

       +----------------------+
       | mart_alerts          |
       +----------------------+

       +----------------------+
       | mart_ml_features     |
       +----------------------+
4. BigQuery Dataset Structure
bronze
├── bronze_sensor_data
├── bronze_machine_master

silver
├── silver_sensor_data
├── silver_machine_master

gold
├── mart_machine_daily_kpi
├── mart_alerts
├── mart_ml_features
5. Bronze Layer Design
Purpose

Raw landing layer.

Rules:

No transformations
No business logic
Preserve source data
Add ingestion timestamp
Table: bronze_sensor_data
Column	Type
id	INT64
machine_id	STRING
temperature	FLOAT64
object_detected_flag	BOOL
buzzer_active_flag	BOOL
created_at	TIMESTAMP
ingestion_timestamp	TIMESTAMP

Partition:

created_at

Source:

Supabase sensor_data_v1
Table: bronze_machine_master
Column	Type
machine_id	STRING
machine_name	STRING
location	STRING
machine_type	STRING
install_date	DATE
installation_engineer_name	STRING
machine_owner_name	STRING
ingestion_timestamp	TIMESTAMP

Source:

Google Drive CSV
6. Silver Layer Design
Purpose

Clean and standardized data layer.

Rules:

Data cleansing
Standardization
Derived columns
Type validation
Table: silver_sensor_data
Source
bronze_sensor_data
Transformations
Remove invalid records
machine_id IS NOT NULL
Standardize temperature
Cast temperature as FLOAT64
Create event_date

Example:

created_at

2026-06-09 18:15:00

becomes

event_date

2026-06-09
Create event_hour

Example:

created_at

2026-06-09 18:15:00

becomes

18
Create event_day_of_week

Example:

Tuesday
Schema
Column	Type
machine_id	STRING
temperature	FLOAT64
object_detected_flag	BOOL
buzzer_active_flag	BOOL
created_at	TIMESTAMP
event_date	DATE
event_hour	INT64
event_day_of_week	STRING

Partition:

event_date

Cluster:

machine_id
Table: silver_machine_master
Source
bronze_machine_master
Transformations
Trim text fields
TRIM()
Standardize names
UPPER()
Calculate machine_age_days

Formula:

Current Date - Install Date

Example:

Install Date = 2025-01-01

Current Date = 2026-06-09

Age = 524 Days
Schema
Column	Type
machine_id	STRING
machine_name	STRING
location	STRING
machine_type	STRING
install_date	DATE
machine_age_days	INT64
installation_engineer_name	STRING
machine_owner_name	STRING

Cluster:

machine_id
7. Data Relationship Model
Parent Table
silver_machine_master

Primary Key:

machine_id
Child Table
silver_sensor_data

Foreign Key:

machine_id

Relationship:

One Machine
     |
     |
     +-------> Many Sensor Events

Example:

MACHINE_001

  ├── Event 1
  ├── Event 2
  ├── Event 3
  ├── Event 4
  └── Event N
8. Gold Layer Design
Purpose

Business-ready datasets.

Gold Table 1
mart_machine_daily_kpi

Purpose:

Operational Dashboard

Source:

silver_sensor_data
JOIN
silver_machine_master

Join Key:

machine_id

Aggregation:

AVG(temperature)

MAX(temperature)

MIN(temperature)

COUNT(*)

SUM(object_detected_flag)

SUM(buzzer_active_flag)

Schema:

Column
event_date
machine_id
machine_name
location
machine_type
avg_temperature
max_temperature
min_temperature
object_detection_count
buzzer_count
total_events
Gold Table 2
mart_alerts

Purpose:

Email Alerting

Source:

silver_sensor_data

Alert Rules:

High Temperature
temperature > 40
Object Detection
object_detected_flag = TRUE
Buzzer Alert
buzzer_active_flag = TRUE

Schema:

Column
alert_id
machine_id
machine_name
location
machine_owner_name
alert_type
alert_severity
alert_message
alert_timestamp
email_sent_flag
Gold Table 3
mart_ml_features

Purpose:

Machine Learning Feature Store

Source:

silver_sensor_data
JOIN
silver_machine_master

Features:

machine_age_days
machine_type
location
avg_temperature
max_temperature
object_detection_count
buzzer_count

Schema:

Column
machine_id
machine_name
machine_type
location
machine_age_days
event_date
event_hour
avg_temperature
max_temperature
object_detection_count
buzzer_count
total_events
9. PySpark Pipeline Design
Job 1
supabase_to_bronze_sensor

Source:

Supabase

Target:

bronze_sensor_data
Job 2
csv_to_bronze_machine_master

Source:

Google Drive CSV

Target:

bronze_machine_master
Job 3
bronze_to_silver_sensor

Source:

bronze_sensor_data

Target:

silver_sensor_data
Job 4
bronze_to_silver_machine_master

Source:

bronze_machine_master

Target:

silver_machine_master
Job 5
silver_to_gold_machine_daily_kpi

Target:

mart_machine_daily_kpi
Job 6
silver_to_gold_alerts

Target:

mart_alerts
Job 7
silver_to_gold_ml_features

Target:

mart_ml_features