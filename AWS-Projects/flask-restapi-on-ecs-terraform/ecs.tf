resource "aws_ecr_repository" "flask_api" {
  name                 = "flask-crud-app"
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "flask-api-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "flask_api" {
  family = "flask-crud-app"
  depends_on = [ null_resource.ecr_image ]
  container_definitions = jsonencode(
    [
      {
        "name" : "flask-crud-app",
        "image" : "${local.repository}:${local.image_version}",
        "essential" : true,
        portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }]
      }
  ])
  cpu                = 256
  execution_role_arn = aws_iam_role.flask_crud_api_ecs_execution_role.arn
  memory             = 512
  network_mode       = "awsvpc"
  
  requires_compatibilities = [
    "FARGATE",
  ]
}

resource "aws_ecs_service" "flask_api" {
  name            = "flask-api"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.flask_api.arn
  desired_count   = 1

}

resource "aws_ecs_service" "flask_api" {
  name            = "flask-api"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.flask_api.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.main.id]
    security_groups = [aws_security_group.main.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.flask_api.arn
    container_name   = "flask-app"
    container_port   = var.container_port
  }

  depends_on = [
    aws_lb_listener.flask_api
  ]
}
