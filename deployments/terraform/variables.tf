variable "project_id" {
  description = "Google Project ID."
  type        = string
}

variable "terraform_service_account_key" {
  description = "Path to terraform service account key"
  type        = string
}

variable "environment_file" {
  description = "Path to environment file to store in secret manager"
  type        = string
}

variable "media_bucket_name" {
  description = "GCS Bucket name. Value should be unique ."
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
}

variable "bucket_region" {
  description = "Google Cloud region"
  type        = string
}

variable "db_tier" {
  description = "Database tier"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "support_email" {
  description = "Support email"
  type        = string
}