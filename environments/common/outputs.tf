output "admin_username" {
  description = "PostgreSQL Admin Username"
  value       = module.postgres.admin_username
  sensitive   = true
}

output "admin_password" {
  description = "PostgreSQL Admin Password"
  value       = module.postgres.admin_password
  sensitive   = true
}

output "postgresql_fqdn" {
  description = "PostgreSQL Fully Qualified Domain Name"
  value       = module.postgres.postgresql_fqdn
}

output "dab_container_app_url" {
  description = "The public URL of the Azure Container App"
  value       = module.dab_service.dab_container_app_url
}