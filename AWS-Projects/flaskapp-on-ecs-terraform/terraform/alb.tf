resource "aws_lb" "alb" {
  name               = "${var.environment}-${var.app_name}-alb"
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

resource "aws_lb_listener" "http_forward" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.alb.arn
  }
}

resource "aws_lb_target_group" "alb" {
  name        = "${var.environment}-${var.app_name}-alb-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "90"
    protocol            = "HTTP"
    matcher             = "200-299"
    timeout             = "20"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

# # Create an HTTPS listener
# resource "aws_lb_listener" "https_forward" {
#   load_balancer_arn  = aws_lb.alb.arn
#   port              = 443
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
#   certificate_arn   = aws_acm_certificate.cert.arn

#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.alb.arn
#   }
# }