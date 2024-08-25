module "layers" {
  for_each = local.layers_info
  source   = "terraform-aws-modules/lambda/aws"
  version  = "7.7.0"

  create_layer = true
  layer_name   = each.key
  description  = each.value.description
  source_path = [
    {
      path             = "${path.module}/${each.value.path}",
      pip_requirements = true,
      prefix_in_zip    = "python"
    },
    {
      path          = "${path.module}/layers/common-scripts",
      prefix_in_zip = "python"
    },

  ]

  runtime                  = lookup(each.value, "runtime", var.lambda_default_settings["runtime"])
  store_on_s3              = true
  s3_prefix                = "layers/${each.key}"
  s3_bucket                = aws_s3_bucket.lambda_artifacts.id
  compatible_architectures = ["x86_64"]
}

# resource "aws_lambda_layer_version_permission" "lambda_layer_permission" {
#   for_each       = local.layers_to_accounts_map
#   layer_name     = module.layers[each.value.layer].lambda_layer_layer_arn
#   version_number = module.layers[each.value.layer].lambda_layer_version
#   principal      = each.value.account
#   action         = "lambda:GetLayerVersion"
#   statement_id   = "${each.value.layer}-${each.value.account}-${random_integer.random.result}"
# }

# resource "random_integer" "random" {
#   min = 1
#   max = 1000
# }
