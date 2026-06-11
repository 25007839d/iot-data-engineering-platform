from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from datetime import datetime
from pathlib import Path

PROJECT_ID = "project-7792d7ca-4ff6-4f52-91b"

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "bigquery" / "mart_machine_daily_kpi.sql") as f:
    machine_daily_kpi_sql = f.read()

with open(BASE_DIR / "bigquery" / "mart_alerts.sql") as f:
    mart_alerts_sql = f.read()

with open(BASE_DIR / "bigquery" / "mart_ml_features.sql") as f:
    mart_ml_features_sql = f.read()


with DAG(
    dag_id="gold_layer_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["gold", "iot"],
) as dag:


    machine_daily_kpi = BigQueryInsertJobOperator(
        task_id="silver_to_gold_machine_daily_kpi",
        configuration={
            "query": {
                "query": machine_daily_kpi_sql,
                "useLegacySql": False,
            }
        },
    )

    mart_alerts = BigQueryInsertJobOperator(
        task_id="silver_to_gold_alerts",
        configuration={
            "query": {
                "query": mart_alerts_sql,
                "useLegacySql": False,
            }
        },
    )

    mart_ml_features = BigQueryInsertJobOperator(
        task_id="silver_to_gold_ml_features",
        configuration={
            "query": {
                "query": mart_ml_features_sql,
                "useLegacySql": False,
            }
        },
    )



    machine_daily_kpi >> mart_alerts>>mart_ml_features
