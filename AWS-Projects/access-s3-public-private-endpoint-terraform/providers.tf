# providers.tf
terraform {
  required_version = "1.5.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.12"
    }
  }
}

provider "aws" {
  region     = var.region
}

# Using local backend
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
