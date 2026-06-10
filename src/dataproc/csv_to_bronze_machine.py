from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("csv_to_bronze_machine")
    .getOrCreate()
)

# ---------------------------------------------------
# Read CSV from GCS
# ---------------------------------------------------
df = (
    spark.read
    .option("header", True)
    .csv(
        "gs://iot-data-lake-dk/row_data/machine_master.csv"
    )
)

# ---------------------------------------------------
# Rename Google Sheet Columns
# ---------------------------------------------------
df = (
    df
    .withColumnRenamed(
        "What is machine name?",
        "machine_name"
    )
    .withColumnRenamed(
        "Location ",
        "location"
    )
    .withColumnRenamed(
        "Machine Type ",
        "machine_type"
    )
    .withColumnRenamed(
        "Install Date ",
        "install_date"
    )
    .withColumnRenamed(
        "Installation Engineer Name",
        "installation_engineer_name"
    )
    .withColumnRenamed(
        "Machine Owner Name",
        "machine_owner_name"
    )
    .withColumnRenamed(
        "What is machine id?",
        "machine_id"
    )
)

# ---------------------------------------------------
# Select Required Columns
# ---------------------------------------------------
df = df.select(
    "machine_id",
    "machine_name",
    "location",
    "machine_type",
    "install_date",
    "installation_engineer_name",
    "machine_owner_name"
)

# ---------------------------------------------------
# Add Audit Column
# ---------------------------------------------------
df = df.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

# ---------------------------------------------------
# Write to BigQuery
# ---------------------------------------------------
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
        "project-7792d7ca-4ff6-4f52-91b.bronze.bronze_machine_master"
    )
    .save()
)