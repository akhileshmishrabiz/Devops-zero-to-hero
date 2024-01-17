# network.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-vpc" })
  )
}

resource "aws_subnet" "public" {
  cidr_block              = var.subnet_cidr_list[0] # 10.0.1.0/24 ->  from ["10.0.1.0/24", "10.0.2.0/24"]
  map_public_ip_on_launch = true                    # only for public subnet
  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${data.aws_region.current.name}a"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public" })
  )
}

resource "aws_subnet" "private" {
  cidr_block        = var.subnet_cidr_list[1] # 10.0.2.0/24 -> from ["10.0.1.0/24", "10.0.2.0/24"]
  vpc_id            = aws_vpc.main.id
  availability_zone = "${data.aws_region.current.name}a"

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private" })
  )
}

# Internet gateway to enable trafic from internet
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-gateway" })
  )
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-public" })
  )
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    local.common_tags,
    tomap({ "Name" = "${local.prefix}-private" })
  )
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# route to internet gateway for public subnet
resource "aws_route" "public_internet_access" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}



