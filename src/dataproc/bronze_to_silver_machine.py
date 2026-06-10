from pyspark.sql import SparkSession
from pyspark.sql.functions import upper
from pyspark.sql.functions import trim
from pyspark.sql.functions import datediff
from pyspark.sql.functions import current_date

spark = (
    SparkSession.builder
    .appName("bronze_to_silver_machine")
    .getOrCreate()
)

df = spark.read \
.format("bigquery") \
.option(
    "table",
    "project-7792d7ca-4ff6-4f52-91b.bronze.bronze_machine_master"
) \
.load()

df = df.withColumn(
    "machine_name",
    upper(trim("machine_name"))
)

df = df.withColumn(
    "machine_age_days",
    datediff(
        current_date(),
        df.install_date
    )
)

df.write \
.mode("overwrite") \
.format("bigquery") \
.option(
    "temporaryGcsBucket",
    "iot-data-lake-dk"
)\
.option(
    "table",
    "project-7792d7ca-4ff6-4f52-91b.silver.silver_machine_master"
) \
.save()