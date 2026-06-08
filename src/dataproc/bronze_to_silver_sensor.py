from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
from pyspark.sql.functions import hour
from pyspark.sql.functions import date_format
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("bronze_to_silver_sensor")
    .getOrCreate()
)

df = spark.read \
.format("bigquery") \
.option(
    "table",
    "project_id.bronze.bronze_sensor_data"
) \
.load()

df = df.filter(
    col("machine_id").isNotNull()
)

df = df.withColumn(
    "event_date",
    to_date("created_at")
)

df = df.withColumn(
    "event_hour",
    hour("created_at")
)

df = df.withColumn(
    "event_day_of_week",
    date_format(
        col("created_at"),
        "EEEE"
    )
)

df.write \
.mode("overwrite") \
.format("bigquery") \
.option(
    "table",
    "project_id.silver.silver_sensor_data"
) \
.save()