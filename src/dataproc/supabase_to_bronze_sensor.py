from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = (
    SparkSession.builder
    .appName("supabase_to_bronze_sensor")
    .getOrCreate()
)

jdbc_url = "jdbc:postgresql://<SUPABASE_HOST>:5432/postgres"

properties = {
    "user": "<USER>",
    "password": "<PASSWORD>",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(
    url=jdbc_url,
    table="sensor_data_v1",
    properties=properties
)

df = df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

df.write \
.mode("overwrite") \
.format("bigquery") \
.option(
    "table",
    "project_id.bronze.bronze_sensor_data"
) \
.save()