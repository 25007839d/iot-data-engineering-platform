resource "google_storage_bucket" "iot_data_lake" {

  name          = "iot-data-lake-dk"

  location      = "ASIA"

  force_destroy = true

  uniform_bucket_level_access = true

}