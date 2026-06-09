from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from datetime import datetime, timedelta



spark = (
    SparkSession.builder
    .appName("supabase_to_bronze_sensor")
    .getOrCreate()
)
# jar file uploaded in gcs at  the time of jo submit we have to pass
# gs://iot-data-lake-dk/jars/postgresql-42.7.3.jar
jdbc_url = (
    "jdbc:postgresql://aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require"
)

properties = {
    "user": "postgres.noatyhntldvoisaqxvip",
    "password": "RWX8smcCG4cG",
    "driver": "org.postgresql.Driver"
}

last_24_hours = (datetime.utcnow() - timedelta(hours=24)
                ).strftime("%Y-%m-%d %H:%M:%S")

query = f"""
(
SELECT *
FROM sensor_data_v1
WHERE created_at >= '{last_24_hours}'
) sensor_data
"""

df = spark.read.jdbc(
    url=jdbc_url,
    table=query,
    properties=properties
)

df = df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

df.write \
.mode("append") \
.format("bigquery") \
.option(
    "table",
    "project_id.bronze.bronze_sensor_data"
) \
.save()