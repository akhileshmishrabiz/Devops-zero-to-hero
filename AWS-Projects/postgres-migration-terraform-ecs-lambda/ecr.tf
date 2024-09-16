resource "aws_ecr_repository" "rds_migration" {
    #checkov:skip=CKV_AWS_136: ECR get auto encrypted
    count                = var.ecr_existing_repository_uri == "" ? 1 : 0
    name                 = "${var.environment}-rds-migration"
    image_tag_mutability = "IMMUTABLE"

    image_scanning_configuration {
        scan_on_push = true
    }
}
