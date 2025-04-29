# DynamoDB Table
resource "aws_dynamodb_table" "url_shortener_table" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "shortId"

  attribute {
    name = "shortId"
    type = "S"
  }

  tags = {
    Name        = var.dynamodb_table_name
    Environment = var.environment
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda
resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.project_name}-lambda-policy"
  description = "Policy for URL Shortener Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Scan"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.url_shortener_table.arn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Lambda function
resource "aws_lambda_function" "url_shortener_lambda" {
  filename         = "lambda.zip"
  function_name    = "${var.project_name}-function"
  role             = aws_iam_role.lambda_role.arn
  handler          = "app.app"
  source_code_hash = filebase64sha256("lambda.zip")
  runtime          = "python3.9"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.url_shortener_table.name
      STAGE          = var.environment
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_policy_attachment]
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "url_shortener_api" {
  name        = "${var.project_name}-api"
  description = "URL Shortener API"
}

# API Gateway Resource for /urls
resource "aws_api_gateway_resource" "urls_resource" {
  rest_api_id = aws_api_gateway_rest_api.url_shortener_api.id
  parent_id   = aws_api_gateway_rest_api.url_shortener_api.root_resource_id
  path_part   = "urls"
}

# API Gateway Method for POST /urls
resource "aws_api_gateway_method" "urls_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id   = aws_api_gateway_resource.urls_resource.id
  http_method   = "POST"
  authorization_type = "NONE"
}

# API Gateway Integration for POST /urls
resource "aws_api_gateway_integration" "urls_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id             = aws_api_gateway_resource.urls_resource.id
  http_method             = aws_api_gateway_method.urls_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.url_shortener_lambda.invoke_arn
}

# API Gateway Method for GET /urls
resource "aws_api_gateway_method" "urls_get_method" {
  rest_api_id   = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id   = aws_api_gateway_resource.urls_resource.id
  http_method   = "GET"
  authorization_type = "NONE"
}

# API Gateway Integration for GET /urls
resource "aws_api_gateway_integration" "urls_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id             = aws_api_gateway_resource.urls_resource.id
  http_method             = aws_api_gateway_method.urls_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.url_shortener_lambda.invoke_arn
}

# API Gateway Resource for /{shortId}
resource "aws_api_gateway_resource" "short_id_resource" {
  rest_api_id = aws_api_gateway_rest_api.url_shortener_api.id
  parent_id   = aws_api_gateway_rest_api.url_shortener_api.root_resource_id
  path_part   = "{shortId}"
}

# API Gateway Method for GET /{shortId}
resource "aws_api_gateway_method" "short_id_get_method" {
  rest_api_id   = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id   = aws_api_gateway_resource.short_id_resource.id
  http_method   = "GET"
  authorization_type = "NONE"
}

# API Gateway Integration for GET /{shortId}
resource "aws_api_gateway_integration" "short_id_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.url_shortener_api.id
  resource_id             = aws_api_gateway_resource.short_id_resource.id
  http_method             = aws_api_gateway_method.short_id_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.url_shortener_lambda.invoke_arn
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.url_shortener_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.url_shortener_api.execution_arn}/*/*/*"
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "url_shortener_deployment" {
  depends_on = [
    aws_api_gateway_integration.urls_post_integration,
    aws_api_gateway_integration.urls_get_integration,
    aws_api_gateway_integration.short_id_get_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.url_shortener_api.id
  stage_name  = var.environment

  lifecycle {
    create_before_destroy = true
  }
}