# output.tf
output "ec2_public_ip" {
  description = "public ip for ec2"
  value       = aws_instance.bastion.public_ip
}

output "s2-bucket-name" {
  value = aws_s3_bucket.s3.id

}