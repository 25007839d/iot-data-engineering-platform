from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from datetime import datetime


PROJECT_ID = "project-7792d7ca-4ff6-4f52-91b"
REGION = "asia-south1"
CLUSTER_NAME = "iot-demo-cluster"


with DAG(
    dag_id="Sensore_master_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:


    bronze_job = DataprocSubmitJobOperator(
        task_id="supabase_to_bronze_sensor",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {
                "cluster_name": CLUSTER_NAME
            },
            "pyspark_job": {
                "main_python_file_uri":
                    "gs://iot-data-lake-dk/spark_script/supabase_to_bronze_sensor.py"
            }
        }
    )

    silver_job = DataprocSubmitJobOperator(
        task_id="bronze_to_silver_sensor",
        project_id=PROJECT_ID,
        region=REGION,
        job={
            "placement": {
                "cluster_name": CLUSTER_NAME
            },
            "pyspark_job": {
                "main_python_file_uri":
                    "gs://iot-data-lake-dk/spark_script/bronze_to_silver_sensor.py"
            }
        }
    )

    bronze_job >> silver_job