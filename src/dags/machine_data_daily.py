from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from datetime import datetime

from google.cloud import storage
import requests

PROJECT_ID = "project-7792d7ca-4ff6-4f52-91b"
REGION = "asia-south1"
CLUSTER_NAME = "iot-demo-cluster"


def drive_to_gcs():

    SHEET_ID = "1Vqay7YnqGtA83aJvf16JTDXPS472N0DZtL-mF-NnPGU"

    BUCKET_NAME = "iot-data-lake-dk"
    GCS_OBJECT = "row_data/machine_master.csv"

    # Export Google Sheet as CSV
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv"
    )

    response = requests.get(url, timeout=60)

    response.raise_for_status()

    # Safety validation
    if "text/html" in response.headers.get("content-type", ""):
        raise Exception(
            "Google Sheet returned HTML instead of CSV. "
            "Check sharing permissions."
        )

    local_file = "/tmp/machine_master.csv"

    with open(local_file, "wb") as f:
        f.write(response.content)

    # Upload to GCS
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)

    blob = bucket.blob(GCS_OBJECT)

    blob.upload_from_filename(
        local_file,
        content_type="text/csv"
    )

    print(
        f"Uploaded gs://{BUCKET_NAME}/{GCS_OBJECT}"
    )


with DAG(
    dag_id="machine_master_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    copy_file = PythonOperator(
        task_id="drive_to_gcs",
        python_callable=drive_to_gcs
    )

    bronze_job = DataprocSubmitJobOperator(
        task_id="csv_to_bronze_machine",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {
                "cluster_name": CLUSTER_NAME
            },
            "pyspark_job": {
                "main_python_file_uri":
                    "gs://iot-data-lake-dk/spark_script/csv_to_bronze_machine.py"
            }
        }
    )

    silver_job = DataprocSubmitJobOperator(
        task_id="bronze_to_silver_machine",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {
                "cluster_name": CLUSTER_NAME
            },
            "pyspark_job": {
                "main_python_file_uri":
                    "gs://iot-data-lake-dk/spark_script/bronze_to_silver_machine.py"
            }
        }
    )

    copy_file >> bronze_job >>silver_job