terraform {
  required_version = "1.8.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.32.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# remote backend
terraform {
  backend "s3" {
    bucket         = "state-bucket-879381241087"
    key            = "lambda-blog/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
  }
}