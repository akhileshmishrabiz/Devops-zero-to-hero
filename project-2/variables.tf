# variables.tf
variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "prefix" {
  default = "main"
}

variable "project" {
  default = "devops-102"
}

variable "contact" {
  default = "akhileshmishra@gmail.com"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "subnet_cidr_list" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "instance_type" {
  default = "t2.micro"
}

variable "keyPath" {
  type    = string
  default = ""
}