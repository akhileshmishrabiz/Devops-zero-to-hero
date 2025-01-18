variable "app_name" {
  type    = string
  default = "flaskapp"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "domain_name" {
  type    = string
  default = "livingdevops.com"

}

##### RDS ############

variable "db_default_settings" {
  type = any
  default = {
    allocated_storage       = 30
    max_allocated_storage   = 50
    engine_version          = 14.15
    instance_class          = "db.t3.micro"
    backup_retention_period = 2
    db_name                 = "postgres"
    ca_cert_name            = "rds-ca-rsa2048-g1"
    db_admin_username       = "postgres"
  }
}


########### microservices #################
#### flask app ####
variable "flask_app_cpu" {
  description = "CPU units for the flask-app service"
  type        = number
  default     = 1024
}

variable "flask_app_memory" {
  description = "Memory in MiB for the flask-app service"
  type        = number
  default     = 2048
}

variable "flask_app_template_file" {
  description = "Template file for the flask-app service"
  type        = string
  default     = "flask-service.json.tpl"
}

variable "flask_app_tag" {
  description = "Tag for the flask-app service"
  type        = string
  default     = "latest"
}

variable "flask_app_container_name" {
  description = "Container name for the flask-app service"
  type        = string
  default     = "flask-app"
}

variable "desired_flask_task_count" {
  description = "Desired count for the flask-app tasks"
  type        = number
  default     = 2

}
