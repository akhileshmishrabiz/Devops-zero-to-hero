locals {
  prefix = var.prefix
  common_tags = {
    Project    = var.project
    Contact    = var.contact
    Managed_by = "Terraform"
  }
}
