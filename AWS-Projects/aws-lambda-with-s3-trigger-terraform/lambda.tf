# Define the Lambda function
resource "aws_lambda_function" "my_lambda_function" {
    function_name    = "my-lambda-function"
    role             = aws_iam_role.lambda_role.arn
    handler          = "main.handler"
    runtime          = "python3.11"
    timeout          = 60
    memory_size      = 128

    # Use the Archive data source to zip the code
    filename         = data.archive_file.lambda_code.output_path
    source_code_hash = data.archive_file.lambda_code.output_base64sha256

    # Define environment variables
    environment {
        variables = {
            "BUCKET_PATH" = "inbound-bucket-custome/incoming/"
        }
    }
}

# Define the IAM role for the Lambda function
resource "aws_iam_role" "lambda_role" {
    name = "my-lambda-role"

    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

# Define the Archive data source to zip the code
data "archive_file" "lambda_code" {
    type        = "zip"
    source_dir  = "lambda_functions/"
    output_path = "lambda_code.zip"
}


# Create an IAM policy for S3 bucket access
resource "aws_iam_policy" "s3_bucket_policy" {
    name        = "s3-bucket-policy"
    description = "Allows read and write access to S3 buckets"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::inbound-bucket-custome/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::inbound-bucket-custome"
        }
    ]
}
EOF
}

# Attach the IAM policy to the Lambda role
resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment" {
    role       = aws_iam_role.lambda_role.name
    policy_arn = aws_iam_policy.s3_bucket_policy.arn
}

# Create an S3 bucket notification configuration
resource "aws_s3_bucket_notification" "lambda_trigger" {
    bucket = "inbound-bucket-custome"

    lambda_function {
        lambda_function_arn = aws_lambda_function.my_lambda_function.arn
        events              = ["s3:ObjectCreated:*"]
        filter_prefix       = "incoming/"
    }
    depends_on = [ aws_lambda_permission.allow_s3_to_invoke_lambda ]
}

# Lambda permissions s3 triger
resource "aws_lambda_permission" "allow_s3_to_invoke_lambda" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::inbound-bucket-custome"
}


# Attach the IAM policy to the S3 bucket
resource "aws_s3_bucket_policy" "s3_bucket_policy" {
    bucket = "inbound-bucket-custome"

    policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::inbound-bucket-custome/*"
            }
        ]
    })
}
