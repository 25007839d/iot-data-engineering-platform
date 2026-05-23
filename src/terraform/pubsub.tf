resource "google_pubsub_topic" "iot_stream_topic" {

  name = "iot-stream-topic"

}

resource "google_pubsub_subscription" "iot_stream_subscription" {

  name  = "iot-stream-subscription"

  topic = google_pubsub_topic.iot_stream_topic.name

}