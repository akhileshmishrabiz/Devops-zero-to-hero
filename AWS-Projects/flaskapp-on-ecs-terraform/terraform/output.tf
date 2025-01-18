output "aws_lb_dns_name" {
  value = aws_lb.alb.dns_name
}
output "db_link" {
  value = aws_secretsmanager_secret.db_link.id
}