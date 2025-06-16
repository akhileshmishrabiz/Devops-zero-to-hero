# zip the code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/iam-key-rotation"
  output_path = "${path.module}/iam-key-rotation.zip"
} 

# iam role
resource "aws_iam_role" "lambda_role" {
  name = "iam-key-rotation-role"
  
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

# iam policy
resource "aws_iam_policy" "lambda_policy" {
  name        = "iam-key-rotation-policy"
  description = "Policy for Lambda function to rotate IAM keys"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "iam:ListAccessKeys",
          "iam:ListUsers",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail",
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# # attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# lambda 
resource "aws_lambda_function" "my_lambda_function" {
    function_name    = "iam-key-rotation"
    role             = aws_iam_role.lambda_role.arn
    handler          = "lambda_function.lambda_handler"
    runtime          = "python3.13"
    timeout          = 60
    memory_size      = 128

    # Use the Archive data source to zip the code
    filename         = data.archive_file.lambda_zip.output_path
    source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}



# cron job part

# create an event
resource "aws_cloudwatch_event_rule" "cron_lambdas" {
  name                = "cronjob"
  description         = "to triggr lambda daily 7.15 pm ist"
  schedule_expression = "cron(40 13 * * ? *)"
}
resource "aws_cloudwatch_event_target" "cron_lambdas" {
  rule = aws_cloudwatch_event_rule.cron_lambdas.name
  arn  = aws_lambda_function.my_lambda_function.arn
}

# Invoke lambda permission
resource "aws_lambda_permission" "cron_lambdas" {
  statement_id  = "key-rotation-lambda-allow"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.my_lambda_function.arn
  source_arn    = aws_cloudwatch_event_rule.cron_lambdas.arn
}