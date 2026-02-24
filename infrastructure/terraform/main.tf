# =============================================================================
# MuleSoft Course Infrastructure — ECS Fargate + NLB
# Training environment: REST API (8090), SOAP Service (8091), PostgreSQL (5432)
# =============================================================================

locals {
  services = {
    rest-api = {
      port       = 8090
      ecr_name   = "${var.project_name}-rest-api"
      log_group  = "/ecs/${var.project_name}/rest-api"
      cpu        = 256
      memory     = 512
      env = [
        { name = "API_KEY", value = var.api_key }
      ]
    }
    soap-service = {
      port       = 8091
      ecr_name   = "${var.project_name}-soap-service"
      log_group  = "/ecs/${var.project_name}/soap-service"
      cpu        = 256
      memory     = 512
      env = [
        { name = "API_KEY", value = var.api_key }
      ]
    }
    postgresql = {
      port       = 5432
      ecr_name   = "${var.project_name}-postgresql"
      log_group  = "/ecs/${var.project_name}/postgresql"
      cpu        = 256
      memory     = 512
      env = [
        { name = "POSTGRES_DB", value = "customer360" },
        { name = "POSTGRES_USER", value = "mulesoft" },
        { name = "POSTGRES_PASSWORD", value = var.db_password }
      ]
    }
  }
}

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

data "aws_availability_zones" "available" {
  state = "available"
}

# -----------------------------------------------------------------------------
# VPC
# -----------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-igw" }
}

# Public subnets (NLB sits here)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = { Name = "${var.project_name}-public-${count.index}" }
}

# Private subnets (ECS tasks run here)
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 10)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "${var.project_name}-private-${count.index}" }
}

# NAT Gateway (single AZ — fine for training)
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = { Name = "${var.project_name}-nat-eip" }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = { Name = "${var.project_name}-nat" }

  depends_on = [aws_internet_gateway.main]
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-public-rt" }
}

resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-private-rt" }
}

resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main.id
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# -----------------------------------------------------------------------------
# Security Groups
# -----------------------------------------------------------------------------

resource "aws_security_group" "nlb" {
  name_prefix = "${var.project_name}-nlb-"
  vpc_id      = aws_vpc.main.id
  description = "NLB - allow classroom access to service ports"

  ingress {
    from_port   = 8090
    to_port     = 8091
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "REST (8090) and SOAP (8091) from classroom"
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "PostgreSQL from classroom"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-nlb-sg" }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "ecs_tasks" {
  name_prefix = "${var.project_name}-ecs-"
  vpc_id      = aws_vpc.main.id
  description = "ECS tasks - accept traffic from NLB only"

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.nlb.id]
    description     = "PostgreSQL from NLB"
  }

  ingress {
    from_port       = 8090
    to_port         = 8091
    protocol        = "tcp"
    security_groups = [aws_security_group.nlb.id]
    description     = "REST + SOAP from NLB"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Outbound for ECR pull, NAT, etc."
  }

  tags = { Name = "${var.project_name}-ecs-sg" }

  lifecycle {
    create_before_destroy = true
  }
}

# -----------------------------------------------------------------------------
# ECR Repositories
# -----------------------------------------------------------------------------

resource "aws_ecr_repository" "services" {
  for_each             = local.services
  name                 = each.value.ecr_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true # Training env — allow terraform destroy to clean up

  tags = { Name = each.value.ecr_name }
}

# -----------------------------------------------------------------------------
# CloudWatch Log Groups
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "services" {
  for_each          = local.services
  name              = each.value.log_group
  retention_in_days = 7

  tags = { Name = "${var.project_name}-${each.key}-logs" }
}

# -----------------------------------------------------------------------------
# IAM — ECS Task Execution Role
# -----------------------------------------------------------------------------

resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = { Name = "${var.project_name}-ecs-execution-role" }
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# -----------------------------------------------------------------------------
# ECS Cluster
# -----------------------------------------------------------------------------

resource "aws_ecs_cluster" "main" {
  name = var.project_name

  setting {
    name  = "containerInsights"
    value = "disabled" # Training env — save costs
  }

  tags = { Name = "${var.project_name}-cluster" }
}

# -----------------------------------------------------------------------------
# NLB + Listeners + Target Groups
# -----------------------------------------------------------------------------

resource "aws_lb" "main" {
  name                             = var.project_name
  load_balancer_type               = "network"
  internal                         = false
  security_groups                  = [aws_security_group.nlb.id]
  subnets                          = [for s in aws_subnet.public : s.id]
  enable_cross_zone_load_balancing = true

  tags = { Name = "${var.project_name}-nlb" }
}

resource "aws_lb_target_group" "services" {
  for_each    = local.services
  name        = "${var.project_name}-${each.key}"
  port        = each.value.port
  protocol    = "TCP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip" # Required for Fargate awsvpc networking

  deregistration_delay = 30 # Fast drain for training

  health_check {
    enabled             = true
    protocol            = "TCP"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = { Name = "${var.project_name}-${each.key}-tg" }
}

resource "aws_lb_listener" "services" {
  for_each          = local.services
  load_balancer_arn = aws_lb.main.arn
  port              = each.value.port
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.services[each.key].arn
  }

  tags = { Name = "${var.project_name}-${each.key}-listener" }
}

# -----------------------------------------------------------------------------
# ECS Task Definitions
# -----------------------------------------------------------------------------

resource "aws_ecs_task_definition" "services" {
  for_each                 = local.services
  family                   = "${var.project_name}-${each.key}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = tostring(each.value.cpu)
  memory                   = tostring(each.value.memory)
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([{
    name      = each.key
    image     = "${aws_ecr_repository.services[each.key].repository_url}:latest"
    essential = true

    portMappings = [{
      containerPort = each.value.port
      protocol      = "tcp"
    }]

    environment = each.value.env

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = each.value.log_group
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])

  tags = { Name = "${var.project_name}-${each.key}-task" }
}

# -----------------------------------------------------------------------------
# ECS Services
# -----------------------------------------------------------------------------

resource "aws_ecs_service" "services" {
  for_each             = local.services
  name                 = each.key
  cluster              = aws_ecs_cluster.main.id
  task_definition      = aws_ecs_task_definition.services[each.key].arn
  desired_count        = 1
  launch_type          = "FARGATE"
  force_new_deployment = true

  load_balancer {
    target_group_arn = aws_lb_target_group.services[each.key].arn
    container_name   = each.key
    container_port   = each.value.port
  }

  network_configuration {
    subnets          = [for s in aws_subnet.private : s.id]
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  depends_on = [aws_lb_listener.services]

  tags = { Name = "${var.project_name}-${each.key}-service" }
}
