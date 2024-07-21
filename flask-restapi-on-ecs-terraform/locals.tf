data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_ecr_authorization_token" "ecr_token" {
  registry_id = data.aws_caller_identity.current.account_id
}
