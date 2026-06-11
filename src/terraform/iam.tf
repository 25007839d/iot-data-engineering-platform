locals {

  iot_platform_roles = [

    "roles/bigquery.admin",
    "roles/storage.admin",
    "roles/pubsub.admin",
    "roles/dataflow.admin",
    "roles/dataproc.admin",
    "roles/composer.admin",
    "roles/composer.user",
    "roles/compute.admin",
    "roles/compute.networkAdmin",
    "roles/secretmanager.admin",
    "roles/logging.admin",
    "roles/logging.logWriter",
    "roles/logging.viewer",
    "roles/resourcemanager.projectIamAdmin",
    "roles/iam.serviceAccountAdmin",
    "roles/iam.serviceAccountUser",
    "roles/iam.serviceAccountKeyAdmin"

  ]

}

resource "google_project_iam_member" "iot_platform_roles" {

  for_each = toset(local.iot_platform_roles)

  project = var.project_id

  role    = each.value

  member  = "serviceAccount:${google_service_account.iot_platform_sa.email}"

}

# ---------------------------------------------------
# Composer Roles
# ---------------------------------------------------

locals {

  composer_roles = [

    "roles/artifactregistry.reader",
    "roles/bigquery.connectionUser",
    "roles/bigquery.jobUser",
    "roles/cloudfunctions.invoker",
    "roles/run.invoker",
    "roles/composer.worker",
    "roles/dataflow.developer",
    "roles/dataflow.worker",
    "roles/iam.serviceAccountUser",
    "roles/dataproc.editor",
    "roles/dataproc.worker",
    "roles/bigquery.dataViewer",
    "roles/bigquery.readSessionUser"

  ]

}

resource "google_project_iam_member" "composer_roles" {

  for_each = toset(local.composer_roles)

  project = var.project_id

  role    = each.value

  member  = "serviceAccount:${google_service_account.composer_service_account.email}"

}

# ---------------------------------------------------
# Dataproc Job Roles
# ---------------------------------------------------

locals {

  dataproc_job_roles = [

  "roles/dataproc.editor",
  "roles/dataproc.worker",

  "roles/storage.objectAdmin",

  "roles/bigquery.dataEditor",
  "roles/bigquery.jobUser",
  "roles/bigquery.readSessionUser",

  "roles/logging.logWriter",
  "roles/monitoring.metricWriter"

]

}

resource "google_project_iam_member" "dataproc_job_roles" {

  for_each = toset(local.dataproc_job_roles)

  project = var.project_id

  role    = each.value

  member  = "serviceAccount:${google_service_account.dataproc_job_sa.email}"

}