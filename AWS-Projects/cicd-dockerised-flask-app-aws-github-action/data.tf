# Fetch the lates AMI (ec2 image) with a given pattern
data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

# Fetch the AWS account ID
data "aws_caller_identity" "current" {}
