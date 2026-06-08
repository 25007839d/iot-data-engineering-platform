from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = (
    SparkSession.builder
    .appName("csv_to_bronze_machine")
    .getOrCreate()
)

df = spark.read \
.option("header", True) \
.csv(
    "gs://iot-landing/machine_master.csv"
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
    "project_id.bronze.bronze_machine_master"
) \
.save()