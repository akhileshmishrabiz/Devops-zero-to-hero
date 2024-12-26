terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
    // Uncomment if you need google-beta
    # google-beta = {
    #   source = "hashicorp/google-beta"
    # }
  }
  required_version = ">= 0.18" 
}