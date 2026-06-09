
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from datetime import datetime, timedelta
import requests
import json

# ---------------------------------------------------
# Spark Session
# ---------------------------------------------------
spark = (
    SparkSession.builder
    .appName("supabase_to_bronze_sensor")
    .getOrCreate()
)

# ---------------------------------------------------
# Supabase Configuration
# ---------------------------------------------------
SUPABASE_URL = "https://noatyhntldvoisaqxvip.supabase.co"

SUPABASE_API_KEY = "sb_publishable_684X-Ts6e7ozMww6pI4dbA_Nwa4f4hz"

TABLE_NAME = "sensor_data_v1"

# ---------------------------------------------------
# Last 24 Hours Filter
# ---------------------------------------------------
last_24_hours = (
    datetime.utcnow() - timedelta(hours=48)
).strftime("%Y-%m-%dT%H:%M:%S")

# ---------------------------------------------------
# Supabase REST API URL
# ---------------------------------------------------
url = (
    f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    f"?select=*"
    f"&created_at=gte.{last_24_hours}"
)

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------
# Read Data from Supabase
# ---------------------------------------------------
response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise Exception(
        f"Supabase API Error: "
        f"{response.status_code} - {response.text}"
    )

records = response.json()

if len(records) == 0:
    print("No records found in last 24 hours.")
    spark.stop()
    exit(0)

# ---------------------------------------------------


from pyspark.sql.functions import (
    current_timestamp,
    col,
    to_timestamp
)
from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    StringType,
    DoubleType,
    BooleanType,
    TimestampType
)

# ---------------------------------------------------
# Create DataFrame
# ---------------------------------------------------
df = spark.createDataFrame(records)

# ---------------------------------------------------
# Add Ingestion Timestamp
# ---------------------------------------------------
df = df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# ---------------------------------------------------
# Data Type Mapping
# ---------------------------------------------------
df = (
    df
    .filter(col("id").isNotNull())
    .filter(col("machine_id").isNotNull())
    .withColumn("id", col("id").cast("long"))
    .withColumn("machine_id", col("machine_id").cast("string"))
    .withColumn("temperature", col("temperature").cast("double"))
    .withColumn("object_detected_flag", col("object_detected_flag").cast("boolean"))
    .withColumn("buzzer_active_flag", col("buzzer_active_flag").cast("boolean"))
    .withColumn("created_at", to_timestamp(col("created_at")))
    .withColumn("ingestion_timestamp", col("ingestion_timestamp").cast("timestamp"))
    .select(
        "id",
        "machine_id",
        "temperature",
        "object_detected_flag",
        "buzzer_active_flag",
        "created_at",
        "ingestion_timestamp"
    )
)

# ---------------------------------------------------
# Explicit BigQuery Schema
# ---------------------------------------------------
target_schema = StructType([
    StructField("id", LongType(), False),                    # REQUIRED
    StructField("machine_id", StringType(), False),          # REQUIRED
    StructField("temperature", DoubleType(), True),
    StructField("object_detected_flag", BooleanType(), True),
    StructField("buzzer_active_flag", BooleanType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("ingestion_timestamp", TimestampType(), True)
])

# Recreate DataFrame with required fields
df = spark.createDataFrame(
    df.rdd,
    schema=target_schema
)

print("===== FINAL SCHEMA =====")
df.printSchema()

print(f"Total Records: {df.count()}")
df.show(10, truncate=False)

# ---------------------------------------------------
# Write to BigQuery Bronze Layer
# ---------------------------------------------------
df.write \
    .mode("append") \
    .format("bigquery") \
    .option(
        "table",
        "project-7792d7ca-4ff6-4f52-91b.bronze.bronze_sensor_data"
    ) \
    .option(
        "temporaryGcsBucket",
        "iot-data-lake-dk"
    ) \
    .save()

print("Data loaded successfully into Bronze Layer")