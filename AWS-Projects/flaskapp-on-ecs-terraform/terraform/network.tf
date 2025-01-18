# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public_1" {
  cidr_block              = "10.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available_zones.names[0]
  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true

  tags = {
    Name = "ECS Fargate Public Subnet 1"
  }
}

resource "aws_subnet" "public_2" {
  cidr_block              = "10.0.3.0/24"
  availability_zone       = data.aws_availability_zones.available_zones.names[1]
  vpc_id                  = aws_vpc.main.id
  map_public_ip_on_launch = true

  tags = {
    Name = "ECS Fargate Public Subnet 2"
  }
}

# Private Subnets for ECS
resource "aws_subnet" "private_1" {
  cidr_block        = "10.0.0.0/24"
  availability_zone = data.aws_availability_zones.available_zones.names[0]
  vpc_id            = aws_vpc.main.id

  tags = {
    Name = "ECS Fargate Private Subnet 1"
  }
}

resource "aws_subnet" "private_2" {
  cidr_block        = "10.0.1.0/24"
  availability_zone = data.aws_availability_zones.available_zones.names[1]
  vpc_id            = aws_vpc.main.id

  tags = {
    Name = "ECS Fargate Private Subnet 2"
  }
}

# RDS Private Subnets
resource "aws_subnet" "rds_1" {
  cidr_block        = "10.0.4.0/24"
  availability_zone = data.aws_availability_zones.available_zones.names[0]
  vpc_id            = aws_vpc.main.id

  tags = {
    Name = "RDS Private Subnet 1"
  }
}

resource "aws_subnet" "rds_2" {
  cidr_block        = "10.0.5.0/24"
  availability_zone = data.aws_availability_zones.available_zones.names[1]
  vpc_id            = aws_vpc.main.id

  tags = {
    Name = "RDS Private Subnet 2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.environment}-igw"
  }
}

# Route for Internet Access
resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.main.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat_1" {
  depends_on = [aws_internet_gateway.main]
  tags = {
    Name = "NAT Gateway EIP 1"
  }
}

resource "aws_eip" "nat_2" {
  depends_on = [aws_internet_gateway.main]
  tags = {
    Name = "NAT Gateway EIP 2"
  }
}

# NAT Gateways
resource "aws_nat_gateway" "nat_1" {
  subnet_id     = aws_subnet.public_1.id
  allocation_id = aws_eip.nat_1.id

  tags = {
    Name = "NAT Gateway 1"
  }
}

resource "aws_nat_gateway" "nat_2" {
  subnet_id     = aws_subnet.public_2.id
  allocation_id = aws_eip.nat_2.id

  tags = {
    Name = "NAT Gateway 2"
  }
}

# Private Route Tables
resource "aws_route_table" "private_1" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_1.id
  }

  tags = {
    Name = "Private Route Table 1"
  }
}

resource "aws_route_table" "private_2" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_2.id
  }

  tags = {
    Name = "Private Route Table 2"
  }
}

# Route Table Associations
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_1.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_2.id
}

resource "aws_security_group" "lb" {
  name        = "${var.environment}-lb-sg"
  vpc_id      = aws_vpc.main.id
  description = "controls access to the Application Load Balancer (ALB)"

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "flask" {
  name        = "${var.environment}-${var.app_name}-sg"
  vpc_id      = aws_vpc.main.id
  description = "allow inbound access from the ALB only"

  ingress {
    protocol        = "tcp"
    from_port       = 8080
    to_port         = 8080
    security_groups = [aws_security_group.lb.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

}
