# Configure the Google Cloud provider
provider "google" {
    credentials = file(var.terraform_service_account_key)
    project     = var.project_id
    region      = var.region
}

# App Engine
resource "google_app_engine_application" "app" {
    project     = var.project_id
    location_id = var.region
}

# Postgres
resource "google_sql_database_instance" "db" {
  name             = var.db_name
  database_version = "POSTGRES_13"
  region           = var.bucket_region

  settings {
    tier = var.db_tier
  }
}

# Cloud Storage - Media Bucket
resource "google_storage_bucket" "media_bucket" {
    name     = var.media_bucket_name
    location = var.bucket_region
}

data "google_app_engine_default_service_account" "default" {}

resource "google_storage_bucket_iam_binding" "binding" {
  bucket = var.media_bucket_name
  role = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:${data.google_app_engine_default_service_account.default.email}",
  ]
}

# Secret Manager

resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
}

resource "google_secret_manager_secret" "django_settings" {
  secret_id = "django_settings"
  replication {
    automatic = true
  }
  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_version" "django_settings-1" {
  secret = google_secret_manager_secret.django_settings.id
  secret_data = file(var.environment_file)
}

resource "google_secret_manager_secret_iam_member" "my-app" {
  secret_id = google_secret_manager_secret.django_settings.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.project_id}@appspot.gserviceaccount.com"
}