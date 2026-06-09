resource "google_dataproc_cluster" "iot_cluster" {

  name   = "iot-demo-cluster"
  region = var.region

  cluster_config {

    gce_cluster_config {
      zone = var.zone
    }

    master_config {

      num_instances = 1

      machine_type = "n4-standard-2"

      disk_config {
        boot_disk_type    = "pd-balanced"
        boot_disk_size_gb = 30
      }
    }

    software_config {
      image_version = "2.2-debian12"
    }
  }
}