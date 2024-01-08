# output.tf
output "ec2_public_ip" {
  description = "public ip for ec2"
  value       = aws_instance.public.public_ip
}