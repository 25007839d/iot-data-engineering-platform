from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG(

    dag_id="iot_pipeline",

    start_date=datetime(
        2026,
        1,
        1
    ),

    schedule="*/15 * * * *",

    catchup=False

) as dag:

    sensor_ingest = BashOperator(
        task_id="sensor_ingest",
        bash_command="""
        spark-submit
        jobs/supabase_to_bronze_sensor.py
        """
    )

    machine_ingest = BashOperator(
        task_id="machine_ingest",
        bash_command="""
        spark-submit
        jobs/csv_to_bronze_machine.py
        """
    )

    sensor_silver = BashOperator(
        task_id="sensor_silver",
        bash_command="""
        spark-submit
        jobs/bronze_to_silver_sensor.py
        """
    )

    machine_silver = BashOperator(
        task_id="machine_silver",
        bash_command="""
        spark-submit
        jobs/bronze_to_silver_machine.py
        """
    )

    sensor_ingest >> sensor_silver

    machine_ingest >> machine_silver