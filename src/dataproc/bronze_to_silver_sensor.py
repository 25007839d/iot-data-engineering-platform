from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    to_date,
    hour,
    date_format,
    col
)

spark = (
    SparkSession.builder
    .appName("bronze_to_silver_sensor")
    .getOrCreate()
)

# Read Bronze Layer
df = (
    spark.read
    .format("bigquery")
    .option(
        "table",
        "project-7792d7ca-4ff6-4f52-91b.bronze.bronze_sensor_data"
    )
    .load()
)

# Data Quality
df = df.filter(
    col("machine_id").isNotNull()
)

# Derived Columns
df = (
    df
    .withColumn(
        "event_date",
        to_date("created_at")
    )
    .withColumn(
        "event_hour",
        hour("created_at")
    )
    .withColumn(
        "event_day_of_week",
        date_format(
            col("created_at"),
            "EEEE"
        )
    )
)

# Write Silver Layer
(
    df.write
    .mode("overwrite")
    .format("bigquery")
    .option(
        "temporaryGcsBucket",
        "iot-data-lake-dk"
    )
    .option(
        "table",
        "project-7792d7ca-4ff6-4f52-91b.silver.silver_sensor_data"
    )
    .save()
)