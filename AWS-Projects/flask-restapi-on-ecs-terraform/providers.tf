terraform {
  required_version = "1.9.2"

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
    bucket         = "my-backend-devops101-terraform"
    key            = "flaskrestapi-onecs/tfstate/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
  }
}
