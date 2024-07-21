# Role to start the task
resource "aws_iam_role" "flask_crud_api_ecs_execution_role" {
  name        = "flask-crud-api-task-execution-role"
  description = "Allows ECS tasks execution"

  assume_role_policy = jsonencode(
    {
      "Version" = "2012-10-17",
      "Statement" = [
        {
          "Action" = "sts:AssumeRole",
          "Principal" = {
            "Service" = "ecs-tasks.amazonaws.com"
          },
          "Effect" = "Allow",
          "Sid" : ""
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.flask_crud_api_ecs_execution_role.name
}