resource "google_service_account" "iot_platform_sa" {

  account_id   = "iot-platform-sa"

  display_name = "IoT Platform Service Account"

}

resource "google_service_account" "composer_service_account" {

  account_id   = "composer-service-account"

  display_name = "Composer Service Account"

}

resource "google_service_account" "dataproc_job_sa" {

  account_id   = "dataproc-job-sa"

  display_name = "Dataproc Job Service Account"

}

