resource "aws_security_group" "rds_shrink_sg" {
  #checkov:skip=CKV2_AWS_5: Will be attached
  name        = "${var.environment}-rds-shrink"
  vpc_id      = ""
  description = "SG for ECS-rds-shrink"

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Access to AWS API"
  }
  lifecycle {
    create_before_destroy = true
  }
  tags = {
    Name = "${var.environment}-rds-shrink"
  }
}