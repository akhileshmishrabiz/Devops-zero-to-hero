# Fetch the AWS account ID
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "lambda_artifacts" {
  bucket = "${data.aws_caller_identity.current.account_id}-lambda-artifacts"
  tags = {
    Name = "lambda-artifacts"
  }
}




# resource "aws_s3_bucket_versioning" "lambda_artifacts" {
#   bucket = aws_s3_bucket.lambda_artifacts.id
#   versioning_configuration {
#     status = "Enabled"
#   }
# }
# resource "aws_s3_bucket_logging" "lambda_artifacts" {
#   bucket        = aws_s3_bucket.lambda_artifacts.id
#   target_bucket = "bucketlog"
#   target_prefix = "${aws_s3_bucket.lambda_artifacts.id}-log/"
# }

# resource "aws_s3_bucket_policy" "lambda_artifacts" {
#   bucket = aws_s3_bucket.lambda_artifacts.id
#   policy = jsonencode({
#     "Version" : "2012-10-17",
#     "Statement" : [
#       {
#         "Effect" : "Deny",
#         "Principal" : "*",
#         "Action" : "*",
#         "Resource" : [
#           "arn:aws:s3:::${aws_s3_bucket.lambda_artifacts.id}/*"
#         ],
#         "Condition" : {
#           "Bool" : {
#             "aws:SecureTransport" : "false"
#           }
#         }
#       }
#     ]
#   })
# }
# resource "aws_s3_bucket_server_side_encryption_configuration" "lambda_artifacts" {
#   bucket = aws_s3_bucket.lambda_artifacts.id

#   rule {
#     apply_server_side_encryption_by_default {
#       sse_algorithm = "AES256"
#     }
#   }
# }

# resource "aws_s3_bucket_public_access_block" "lambda_artifacts" {
#   bucket = aws_s3_bucket.lambda_artifacts.id

#   block_public_acls       = true
#   block_public_policy     = true
#   ignore_public_acls      = true
#   restrict_public_buckets = true
# }

# resource "aws_s3_bucket_lifecycle_configuration" "lambda_artifacts" {
#   bucket = aws_s3_bucket.lambda_artifacts.id
#   rule {
#     id     = "managed"
#     status = "Enabled"
#     transition {
#       days          = var.s3_default_settings.lifecycle_transition_oia_days
#       storage_class = "ONEZONE_IA"
#     }
#     noncurrent_version_expiration {
#       noncurrent_days = var.s3_default_settings.lifecycle_noncurrent_expiration_days
#     }
#     abort_incomplete_multipart_upload {
#       days_after_initiation = 1
#     }
#   }
# }