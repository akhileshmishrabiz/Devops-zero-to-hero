# Role inherited by the task
resource "aws_iam_role" "rds_migration_ecs_task_role" {
    name        = "${var.environment}-rds-migration-ecs-role"
    description = "Allows ECS tasks to call AWS services"

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
                }
            ]
        }
    )
}

resource "aws_iam_policy" "rds_migration_ecs_task_policy" {
    name = "${var.environment}-rds-migration-task-role-policy"

    policy = jsonencode(
        {
            "Version" : "2012-10-17",
            "Statement" : [
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    "Resource" : [aws_cloudwatch_log_group.rds_migration.arn]
                },
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "kms:*"
                    ],
                    "Resource" : [
                        data.aws_kms_key.rds_kms_key.arn,
                        data.aws_kms_key.env_kms_key.arn
                    ]
                },
                {
                    "Effect" : "Allow",
                    "Action" : [
                        "rds:DescribeDBInstances",
                        "rds:DescribeDBClusters",
                        "rds:CreateDBInstance",
                        "rds:AddTagsToResource",
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress",
                        "ec2:RevokeSecurityGroupEgress",
                        "ec2:RevokeSecurityGroupIngress",
                        "ssm:DescribeParameters",
                        "ssm:GetParameter",
                        "ssm:GetParameters",
                        "cloudwatch:GetMetricData",
                        "rds:ModifyDBInstance",
                        "rds:StopDBInstance"

                    ],
                    "Resource" : "*"
                },
            ]
    })
}

resource "aws_iam_role_policy_attachment" "rds_migration_ecs_task_policy" {
    role       = aws_iam_role.rds_migration_ecs_task_role.name
    policy_arn = aws_iam_policy.rds_migration_ecs_task_policy.arn
}

# Role to start the task
resource "aws_iam_role" "rds_migration_ecs_execution_role" {
    name        = "${var.environment}rds-migration-task-execution-role"
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
    role       = aws_iam_role.rds_migration_ecs_execution_role.name
}