# iam.tf
resource "aws_iam_role" "ec2" {
  name = "ec2_docker"
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

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-docker-profile"
  role = aws_iam_role.ec2.name
}

# Using aws managed policy to enable ec2 access ECR-> EC2InstanceProfileForImageBuilderECRContainerBuilds
# use custom policy in the production
resource "aws_iam_role_policy_attachment" "bastion" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/EC2InstanceProfileForImageBuilderECRContainerBuilds"
}
