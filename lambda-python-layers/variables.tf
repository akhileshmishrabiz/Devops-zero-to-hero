variable "lambda_default_settings" {
  type = object({
    timeout             = number
    runtime             = string
    compatible_runtimes = list(string)
  })
  default = {
    timeout             = 10
    runtime             = "python3.10"
    compatible_runtimes = ["python3.9", "python3.10", "python3.11"]
  }
}


# variable "s3_default_settings" {
#   type = object({
#     lifecycle_transition_oia_days        = number
#     lifecycle_noncurrent_expiration_days = number
#   })
#   default = {
#     lifecycle_transition_oia_days        = 30
#     lifecycle_noncurrent_expiration_days = 90
#   }
# }