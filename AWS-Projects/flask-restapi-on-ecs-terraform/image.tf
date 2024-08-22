locals {
  repository    = aws_ecr_repository.flask_api.repository_url
  image_version = "v${substr(null_resource.new_tag.id, 0, 15)}"
}

resource "time_rotating" "ecr_image" {
  rotation_days = 30
}

data "archive_file" "image_change_detection" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/src.zip"
}

resource "null_resource" "new_tag" {
  triggers = {
    timer    = time_rotating.ecr_image.id
    src_hash = data.archive_file.image_change_detection.output_sha
  }
}

resource "null_resource" "ecr_image" {
  depends_on = [
    aws_ecr_repository.flask_api
  ]
  triggers = {
    src_hash = data.archive_file.image_change_detection.output_sha
  }

  provisioner "local-exec" {
    environment = {
      AWS_DEFAULT_REGION = data.aws_region.current.name
    }
    command = <<Settings
      cd ${path.module}/src
      chmod u+x ../docker-build.sh
      ../docker-build.sh '${aws_ecr_repository.flask_api.repository_url}' '${data.aws_ecr_authorization_token.ecr_token.password}' v${substr(null_resource.new_tag.id, 0, 15)}
    Settings
  }
}
