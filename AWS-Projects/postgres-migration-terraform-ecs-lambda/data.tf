data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_kms_key" "environment_kms" {
  key_id = "alias/rbscdd-${var.environment}-kms"
}

data "aws_vpc" "vpc" {
  filter {
    name   = "tag:Name"
    values = ["rbscdd-${var.environment}"]
  }
  # vpc id can be refrenced as -split("vpc/", data.aws_vpc.vpc.arn)[1] 
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [split("vpc/", data.aws_vpc.vpc.arn)[1]]
  }
  filter {
    name   = "tag:Name"
    values = ["rbscdd-${var.environment}-private"]
  }
}

data "aws_subnet" "private" {
  for_each = toset(data.aws_subnets.private.ids)
  id       = each.value
  # to access subnet list -> [for subnet_id, subnet in data.aws_subnet.private :  subnet.id]
}

data "aws_kms_key" "rds_kms_key" {
  key_id = "alias/rbscdd-${var.environment}-db"
}


data "aws_kms_key" "env_kms_key" {
  key_id = "alias/rbscdd-${var.environment}-kms"
}