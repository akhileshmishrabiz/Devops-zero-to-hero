resource "aws_ecr_repository" "flask" {
  name                 = "docker-flask"


# Enable in production -> this will scan all docker images for vulnerabilities
#   image_scanning_configuration {
#     scan_on_push = true
#   }
}