output "bucket_name" {

  value = google_storage_bucket.iot_data_lake.name

}

output "pubsub_topic" {

  value = google_pubsub_topic.iot_stream_topic.name

}

output "service_account_email" {

  value = google_service_account.iot_platform_sa.email

}