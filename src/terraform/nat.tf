# NAT use for provide access on public ip to connect internet

resource "google_compute_router" "nat_router" {
  name    = "dataproc-router"
  region  = "asia-south1"
  network = "default"
}

resource "google_compute_router_nat" "dataproc_nat" {
  name                               = "dataproc-nat"
  router                             = google_compute_router.nat_router.name
  region                             = google_compute_router.nat_router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}