resource "aws_ecr_repository" "flask_app" {
  name = "${var.environment}-${var.app_name}"
}