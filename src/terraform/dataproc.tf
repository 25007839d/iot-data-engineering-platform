resource "google_dataproc_cluster" "iot_cluster" {

  name   = "iot-demo-cluster"
  region = var.region

  cluster_config {

    gce_cluster_config {

      zone = var.zone

      service_account = google_service_account.dataproc_job_sa.email

      internal_ip_only = false
    }

    master_config {

      num_instances = 1

      machine_type = "e2-standard-2"

      disk_config {

        boot_disk_size_gb = 30
      }
    }
  }
}