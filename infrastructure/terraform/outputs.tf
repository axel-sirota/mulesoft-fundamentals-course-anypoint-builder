output "nlb_dns_name" {
  description = "NLB DNS name — students use this as the infrastructure host"
  value       = aws_lb.main.dns_name
}

output "rest_api_url" {
  description = "REST Enrichment API base URL"
  value       = "http://${aws_lb.main.dns_name}:8090"
}

output "soap_wsdl_url" {
  description = "SOAP Address Validation WSDL URL"
  value       = "http://${aws_lb.main.dns_name}:8091/?wsdl"
}

output "postgresql_host" {
  description = "PostgreSQL connection host (NLB DNS)"
  value       = aws_lb.main.dns_name
}

output "postgresql_port" {
  description = "PostgreSQL connection port"
  value       = 5432
}

output "ecr_repository_urls" {
  description = "ECR repository URLs for docker push"
  value       = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}

output "student_application_properties" {
  description = "Copy-paste block for students' application.properties"
  value       = <<-EOT
    # Infrastructure Connection Properties (Module 4)
    # Host: ${aws_lb.main.dns_name}
    enrichment.api.host=${aws_lb.main.dns_name}
    enrichment.api.port=8090
    enrichment.api.basePath=/api
    db.host=${aws_lb.main.dns_name}
    db.port=5432
    db.name=customer360
    db.user=mulesoft
    db.password=REPLACE_WITH_PASSWORD_FROM_INSTRUCTOR
    soap.address.wsdl=http://${aws_lb.main.dns_name}:8091/?wsdl
  EOT
}
