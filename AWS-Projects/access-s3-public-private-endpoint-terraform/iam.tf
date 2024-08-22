# iam.tf
#creating role for bastion server to access S3 
resource "aws_iam_role" "bastion_role" {
  name = "${local.prefix}-bastion_server"
  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_instance_profile" "bastion_profile" {
  name = "bastion-profile"
  role = aws_iam_role.bastion_role.name
}

# IAM Policy for S3 Access
resource "aws_iam_policy" "s3_access_policy" {
  name        = "EC2S3AccessPolicy"
  description = "Policy to allow EC2 instance to access S3 bucket"

  # Specify the required S3 permissions
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${aws_s3_bucket.s3.arn}/*",
        "arn:aws:s3:::${aws_s3_bucket.s3.arn}"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "bastion" {
  role       = aws_iam_role.bastion_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}
