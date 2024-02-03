# Public ec2
resource "aws_instance" "private" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  availability_zone      = "${var.region}a"
  vpc_security_group_ids = [aws_security_group.docker_on_ec2.id, ]
  key_name               = var.ssh_key
  
  # User data script to configure docker 
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl enable docker
              systemctl start docker
              usermod -a -G docker ec2-user

              EOF

  tags = {
     "Name" = "docker-ec2-instance" 
     }

}

# security group
resource "aws_security_group" "docker_on_ec2" {
  description = "allow ssh to ec2"
  name        = "docker-on-ec2"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


