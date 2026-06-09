from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator

from datetime import datetime

PROJECT_ID = "project-7792d7ca-4ff6-4f52-91b"
REGION = "asia-south1"
CLUSTER_NAME = "iot-demo-cluster"

CLUSTER_CONFIG = {

    "gce_cluster_config": {

        "zone_uri": "asia-south1-a",

        "service_account":
        "dataproc-job-sa@project-7792d7ca-4ff6-4f52-91b.iam.gserviceaccount.com",

        "internal_ip_only": False
    },

    "master_config": {

        "num_instances": 1,

        "machine_type_uri": "e2-standard-4",

        "disk_config": {

            "boot_disk_size_gb": 30
        }
    }
}
with DAG(
    dag_id="create_dataproc_cluster",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        cluster_config=CLUSTER_CONFIG
    )
