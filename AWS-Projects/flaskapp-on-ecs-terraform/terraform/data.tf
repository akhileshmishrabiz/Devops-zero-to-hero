data "aws_availability_zones" "available_zones" {
  state = "available"
}

data "aws_rds_engine_version" "postgresql" {
  engine  = "postgres"
  version = lookup(var.db_default_settings.engine_version, "engine_version", "14.10")
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}