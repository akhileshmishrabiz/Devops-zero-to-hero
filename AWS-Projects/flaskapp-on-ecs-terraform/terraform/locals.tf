locals {

  flask_ecs_services_vars = {
    aws_ecr_repository            = aws_ecr_repository.flask_app.repository_url
    tag                           = var.flask_app_tag
    container_name                = var.flask_app_container_name
    aws_cloudwatch_log_group_name = "/aws/ecs/${var.environment}-${var.app_name}"
    database_url                  = "postgresql://${aws_db_instance.postgres.username}:${random_password.dbs_random_string.result}@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${aws_db_instance.postgres.db_name}"
    environment                   = var.environment
    db_link_secret                = aws_secretsmanager_secret.db_link.id
    db_host                       = aws_db_instance.postgres.address
  }

  app_deploy_data = {
    IMAGE_NAME : "${var.app_name}-image"
    ECR_REGISTRY : "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com"
    ECR_REPOSITORY : "${var.environment}-${var.app_name}"
    ACCOUNT_ID : data.aws_caller_identity.current.account_id
    ECS_CLUSTER : "${var.environment}-${var.app_name}-cluster"
    ECS_REGION : data.aws_region.current.name
    ECS_SERVICE : "${var.environment}-${var.app_name}-service"
    ECS_TASK_DEFINITION : "${var.environment}-${var.app_name}-flask"
    ECS_APP_CONTAINER_NAME : var.flask_app_container_name

  }
}


resource "aws_secretsmanager_secret" "app_deploy_data" {
  name        = "${var.environment}-${var.app_name}-deploy-data"
  description = "Deployment data for the Flask app"
}

resource "aws_secretsmanager_secret_version" "app_deploy_data_version" {
  secret_id     = aws_secretsmanager_secret.app_deploy_data.id
  secret_string = jsonencode(local.app_deploy_data)
}