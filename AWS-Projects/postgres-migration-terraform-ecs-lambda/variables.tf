variable "environment" {
  type = string
}

variable "gpg_runner_sizes" {
  type = map(any)
  default = {
    "cpu" : 256
    "memory" : 2048
  }
}


variable "ecr_existing_repository_uri" {
  type    = string
  default = ""
}

variable "ecr_shared_account_ids" {
  type    = list(string)
  default = []
}

variable "log_retention_days" {
  type    = number
  default = 30
}

variable "lifecycle_expiration_days" {
  type    = number
  default = 30
}

variable "lifecycle_transition_oia_days" {
  type    = number
  default = 30
}

variable "lifecycle_noncurrent_expiration_days" {
  type    = number
  default = 30

}

variable "ecs_container" {
  type    = string
  default = "rds-migration"
}