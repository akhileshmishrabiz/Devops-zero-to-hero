[
  {
    "name": "${container_name}",
    "image": "${aws_ecr_repository}:${tag}",
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "ap-south-1",
        "awslogs-stream-prefix": "${aws_cloudwatch_log_group_name}-service",
        "awslogs-group": "${aws_cloudwatch_log_group_name}"
      }
    },
    "portMappings": [
      {
        "containerPort": 8080,
        "hostPort": 8080,
        "protocol": "tcp",
        "name": "app",
        "appProtocol": "http"
      }
    ],
    "secrets": [
                {
                    "name": "DATABASE_URL",
                    "valueFrom": "${database_url}"
                }
            ],
    "environment": [
      {
        "name": "ENV",
        "value": "${environment}"
      },
      {
        "name": "DB_LINK",
        "value": "${db_link_secret}"
      },
      {
        "name": "DB_HOST",
        "value": "${db_host}"
      }
    ]
  }
]