locals {
    repository    = var.ecr_existing_repository_uri == "" ? aws_ecr_repository.rds_migration[0].repository_url : split(":", var.ecr_existing_repository_uri)[0]
    image_version = var.ecr_existing_repository_uri == "" ? "v${substr(null_resource.new_tag[0].id, 0, 15)}" : split(":", var.ecr_existing_repository_uri)[1]
}

resource "null_resource" "ecr_image" {
    count = var.ecr_existing_repository_uri == "" ? 1 : 0
    depends_on = [
        aws_ecr_repository.rds_migration
    ]
    triggers = {
        timer    = time_rotating.ecr_image[0].id
        src_hash = data.archive_file.image_change_detection[0].output_sha
    }

    provisioner "local-exec" {
        environment = {
            AWS_DEFAULT_REGION = data.aws_region.current.name
        }
        command = <<Settings
            cd ${path.module}/image/
            ../awsdocker.sh '${aws_ecr_repository.rds_migration[0].repository_url}' '${data.aws_ecr_authorization_token.ecr_token[0].password}' v${substr(null_resource.new_tag[0].id, 0, 15)}
        Settings
        # interpreter = [var.interpretter, "-Command"]
    }
}
