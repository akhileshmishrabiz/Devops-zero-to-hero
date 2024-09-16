resource "aws_cloudwatch_log_group" "rds_migration" {
    #checkov:skip=CKV_AWS_158: CWL get auto encrypted
    name              = "/aws/ecs/${var.environment}-rds-migration"
    retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_query_definition" "rds_migration_logs" {
    name = "${var.environment}/rds-migration"

    log_group_names = [
        aws_cloudwatch_log_group.rds_migration.name,
    ]

    query_string = <<EOF
filter @message not like /.+Waiting.+/
| fields @timestamp, @message
| sort @timestamp desc
| limit 200
EOF
}

resource "aws_ecs_cluster" "ecs_cluster" {
    name = "${var.environment}rds-migration"

    setting {
        name  = "containerInsights"
        value = "enabled"
    }
}

resource "aws_ecs_task_definition" "rds_migration" {
    #checkov:skip=CKV_AWS_336: The ECS task needs write access to system
    family     = "${var.environment}-rds-migration"
    depends_on = [null_resource.ecr_image]
    container_definitions = jsonencode(
        [
            {
                "name" : var.ecs_container,
                "image" : "${local.repository}:${local.image_version}",
                "essential" : true,
                "logConfiguration" : {
                    "logDriver" : "awslogs",
                    "options" : {
                        "awslogs-group" : aws_cloudwatch_log_group.rds_migration.name,
                        "awslogs-region" : data.aws_region.current.name,
                        "awslogs-stream-prefix" : "ecs"
                    },
                },
                "environment" : [
                    {
                        "name" : "SG_ID",
                        "value" : aws_security_group.rds_migration_sg.id
                    },
                    {
                        "name" : "ENVIRONMENT",
                        "value" : var.environment
                    },
                ]
            }
    ])

    cpu                = var.gpg_runner_sizes.cpu
    execution_role_arn = aws_iam_role.rds_migration_ecs_execution_role.arn
    memory             = var.gpg_runner_sizes.memory
    network_mode       = "awsvpc"
    requires_compatibilities = [
        "FARGATE",
    ]
    task_role_arn = aws_iam_role.rds_migration_ecs_task_role.arn

    ephemeral_storage {
        size_in_gib = 30
    }
}