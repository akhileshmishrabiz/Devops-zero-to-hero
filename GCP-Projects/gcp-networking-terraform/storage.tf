resource "google_storage_bucket" "remote-backend" {
  project                     = var.project_id
  name                        = tfstate-bucket
  uniform_bucket_level_access = true
  location                    = var.region

  versioning {
    enabled = true
  }
}

resource "google_storage_bucket_iam_member" "remote" {
  bucket = google_storage_bucket.remote-backend.name
  role   = "roles/storage.admin"
  member = "serviceAccount:somesvc@someproject.iam.gserviceaccount.com"
}