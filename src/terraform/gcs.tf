resource "google_storage_bucket" "iot_data_lake" {

  name          = "iot-data-lake-dk"

  location      = "ASIA"

  force_destroy = true

  uniform_bucket_level_access = true

}

# ========== bucket object
# Existing Bucket
resource "google_storage_bucket_object" "spark_scripts_folder" {
  name    = "spark_script/"
  bucket  = "iot-data-lake-dk"
  content = " "
}

resource "google_storage_bucket_object" "raw_data_folder" {
  name    = "row_data/"
  bucket  = "iot-data-lake-dk"
  content = " "
}
