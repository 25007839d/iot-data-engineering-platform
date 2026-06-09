# latest testing ke baad conclusion ye hai ki Dataproc cluster successfully internet aur Supabase dono se connect ho raha hai. Cluster initially internalIpOnly=true ke saath create hua tha, isliye network/NAT issue suspect kiya gaya, lekin master node se curl https://google.com aur curl https://noatyhntldvoisaqxvip.supabase.co successfully execute hue, jisse confirm hua ki external connectivity available hai. Supabase Data API bhi local environment se successfully access hui. Isliye current blocker network, firewall, Cloud NAT ya Supabase reachability nahi hai; remaining failures likely PySpark application code, API authentication/configuration, endpoint/table reference, job packaging, ya Dataproc par outdated script execution se related hain.

resource "google_dataproc_cluster" "iot_cluster" {

  name   = "iot-demo-cluster"
  region = var.region

  cluster_config {

    gce_cluster_config {
      zone            = var.zone
      service_account = google_service_account.dataproc_job_sa.email
      internal_ip_only = false
    }

    master_config {
      num_instances = 1
      machine_type  = "e2-standard-2"

      disk_config {
        boot_disk_size_gb = 30
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = "e2-standard-2"

      disk_config {
        boot_disk_size_gb = 30
      }
    }
  }
}