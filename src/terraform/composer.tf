resource "google_composer_environment" "iot_composer" {

  name   = "iot-composer"

  region = var.region

  config {

    node_config {

      service_account = google_service_account.composer_service_account.email
    }

    workloads_config {

      scheduler {
        cpu        = 0.5
        memory_gb  = 2
        storage_gb = 1
        count      = 1
      }

      web_server {
        cpu        = 0.5
        memory_gb  = 2
        storage_gb = 1
      }

      worker {
        cpu        = 0.5
        memory_gb  = 2
        storage_gb = 2
        min_count  = 1
        max_count  = 1
      }
    }

    software_config {

      image_version = "composer-3-airflow-2.10.5"
    }
  }
}