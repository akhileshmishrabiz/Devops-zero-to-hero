data "archive_file" "lambda_function_zip" {
    type        = "zip"
    source_dir  = "${path.module}/functions/rds-migration-ecs-trigger-lambda"
    output_path = "${path.module}/rds-migration-lambda.zip"
}


resource "aws_lambda_function" "lambda_function" {
    function_name    = "${var.environment}-rds-migration-lambda"
    role             = aws_iam_role.lambda_exec.arn
    handler          = "main.handler"
    runtime          = "python3.11"
    filename         = "${path.module}/rds-migration-lambda.zip"
    depends_on       = [data.archive_file.lambda_function_zip]
    source_code_hash = data.archive_file.lambda_function_zip.output_base64sha256

    environment {
        variables = {
            ECS_CLUSTER   = aws_ecs_cluster.ecs_cluster.name
            ECS_TASK_DEF  = aws_ecs_task_definition.rds_migration.arn
            ECS_CONTAINER = var.ecs_container
            VPC           = split("vpc/", data.aws_vpc.vpc.arn)[1]
            SUBNET_GROUP  = jsonencode([for subnet_id, subnet in data.aws_subnet.private : subnet.id])
            SG            = aws_security_group.rds_migration_sg.id
        }
    }
}

resource "aws_iam_role" "lambda_exec" {
    name = "rbscdd-rds-migration-lambda-execution-${var.environment}"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Action = "sts:AssumeRole",
                Effect = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com",
                },
            },
        ],
    })
}

resource "aws_iam_policy_attachment" "lambda_attach" {
    name       = "rbscdd-rds-migration-lambda-attach-${var.environment}"
    policy_arn = aws_iam_policy.lambda.arn
    roles      = [aws_iam_role.lambda_exec.name]
}

resource "aws_iam_policy" "lambda" {
    name        = "rbscdd-rds-migration-lambda-policy-${var.environment}"
    description = "IAM policy for the Lambda function"

    policy = jsonencode(
        {
            "Version" : "2012-10-17",
            "Statement" : [
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "kms:Decrypt",
                        "kms:GenerateDataKey",
                    ],
                    "Resource" : [
                        "*"
                    ]
                },
                {
                    "Effect" : "Allow",
                    "Action" : "logs:CreateLogGroup",
                    "Resource" : "*"
                },
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "iam:PassRole",
                        "ecs:RunTask",
                    ],
                    "Resource" : "*"
                },
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource" : "*"
                }
            ]
        }
    )
}
