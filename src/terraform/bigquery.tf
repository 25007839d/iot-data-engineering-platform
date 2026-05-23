# Bronze Dataset
resource "google_bigquery_dataset" "bronze" {

  dataset_id = "bronze"

  location   = var.region

}

# Silver Dataset
resource "google_bigquery_dataset" "silver" {

  dataset_id = "silver"

  location   = var.region

}

# Gold Dataset
resource "google_bigquery_dataset" "gold" {

  dataset_id = "gold"

  location   = var.region

}

##Bronze Sensor Raw Table
resource "google_bigquery_table" "sensor_data_raw" {

  dataset_id = google_bigquery_dataset.bronze.dataset_id

  table_id = "sensor_data_raw"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/bronze/sensor_data_raw.json"
  )

}
resource "google_bigquery_table" "machine_master_raw" {

  dataset_id = google_bigquery_dataset.bronze.dataset_id

  table_id = "machine_master_raw"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/bronze/machine_master_raw.json"
  )

}

##SILVER TABLES
resource "google_bigquery_table" "sensor_data" {

  dataset_id = google_bigquery_dataset.silver.dataset_id

  table_id = "sensor_data"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/silver/sensor_data.json"
  )

}
resource "google_bigquery_table" "machine_master" {

  dataset_id = google_bigquery_dataset.silver.dataset_id

  table_id = "machine_master"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/silver/machine_master.json"
  )

}

##GOLD TABLES

resource "google_bigquery_table" "machine_health_metrics" {

  dataset_id = google_bigquery_dataset.gold.dataset_id

  table_id = "machine_health_metrics"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/gold/machine_health_metrics.json"
  )

}
resource "google_bigquery_table" "predictive_alerts" {

  dataset_id = google_bigquery_dataset.gold.dataset_id

  table_id = "predictive_alerts"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/gold/predictive_alerts.json"
  )

}