variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "api_key" {
  description = "API key for REST and SOAP services — delivered to students in class"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "PostgreSQL password for the mulesoft user"
  type        = string
  sensitive   = true
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the NLB (classroom IP range)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "project_name" {
  description = "Prefix for all resource names"
  type        = string
  default     = "mulesoft-course"
}
