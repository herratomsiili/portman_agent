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
