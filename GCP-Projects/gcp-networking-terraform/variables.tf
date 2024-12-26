variable "region" {
  type        = string
  description = "The region for subnet"
}
variable "subnetwork_name" {
  type        = string
  description = "The name of the subnetwork"
}
variable "vpc_name" {
  type        = string
  description = "The name of the VPC network"
}
variable "project_id" {
  type        = string
  description = "GCP project id"
}
variable "subnet_cidr" {
  type        = string
  description = "CIDR range for subnet"
}