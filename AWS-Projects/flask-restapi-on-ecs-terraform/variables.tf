variable "region" {
  description = "AWS region"
  default     = "us-west-2"
}

variable "vpc_id" {
  description = "VPC ID where ECS and ALB will be deployed"
}

variable "subnets" {
  description = "List of subnets for ALB"
  type        = list(string)
}

variable "app_name" {
  description = "Name of the application"
  default     = "my-app"
}

variable "container_port" {
  description = "Port on which the container listens"
  default     = 5000
}
