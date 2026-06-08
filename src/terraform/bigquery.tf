# ------------------------------------------------------------------
# DATASETS
# ------------------------------------------------------------------

resource "google_bigquery_dataset" "bronze" {
  dataset_id = "bronze"
  location   = var.region
}

resource "google_bigquery_dataset" "silver" {
  dataset_id = "silver"
  location   = var.region
}

resource "google_bigquery_dataset" "gold" {
  dataset_id = "gold"
  location   = var.region
}

# ------------------------------------------------------------------
# BRONZE TABLES
# ------------------------------------------------------------------

resource "google_bigquery_table" "bronze_sensor_data" {

  dataset_id = google_bigquery_dataset.bronze.dataset_id
  table_id   = "bronze_sensor_data"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/bronze/bronze_sensor_data.json"
  )

  time_partitioning {
    type  = "DAY"
    field = "created_at"
  }
}

resource "google_bigquery_table" "bronze_machine_master" {

  dataset_id = google_bigquery_dataset.bronze.dataset_id
  table_id   = "bronze_machine_master"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/bronze/bronze_machine_master.json"
  )
}

# ------------------------------------------------------------------
# SILVER TABLES
# ------------------------------------------------------------------

resource "google_bigquery_table" "silver_sensor_data" {

  dataset_id = google_bigquery_dataset.silver.dataset_id
  table_id   = "silver_sensor_data"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/silver/silver_sensor_data.json"
  )

  time_partitioning {
    type  = "DAY"
    field = "event_date"
  }

  clustering = [
    "machine_id"
  ]
}

resource "google_bigquery_table" "silver_machine_master" {

  dataset_id = google_bigquery_dataset.silver.dataset_id
  table_id   = "silver_machine_master"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/silver/silver_machine_master.json"
  )

  clustering = [
    "machine_id"
  ]
}

# ------------------------------------------------------------------
# GOLD TABLES
# ------------------------------------------------------------------

resource "google_bigquery_table" "mart_machine_daily_kpi" {

  dataset_id = google_bigquery_dataset.gold.dataset_id
  table_id   = "mart_machine_daily_kpi"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/gold/mart_machine_daily_kpi.json"
  )

  time_partitioning {
    type  = "DAY"
    field = "event_date"
  }

  clustering = [
    "machine_id"
  ]
}

resource "google_bigquery_table" "mart_alerts" {

  dataset_id = google_bigquery_dataset.gold.dataset_id
  table_id   = "mart_alerts"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/gold/mart_alerts.json"
  )

  time_partitioning {
    type  = "DAY"
    field = "alert_timestamp"
  }
}

resource "google_bigquery_table" "mart_ml_features" {

  dataset_id = google_bigquery_dataset.gold.dataset_id
  table_id   = "mart_ml_features"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/gold/mart_ml_features.json"
  )

  time_partitioning {
    type  = "DAY"
    field = "event_date"
  }

  clustering = [
    "machine_id"
  ]
}