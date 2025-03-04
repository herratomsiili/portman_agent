# Output Database Connection Details
output "postgresql_fqdn" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "admin_username" {
  value     = azurerm_postgresql_flexible_server.postgres.administrator_login
  sensitive = true
}

output "admin_password" {
  value     = azurerm_postgresql_flexible_server.postgres.administrator_password
  sensitive = true
}

output "postgres_server_id" {
  description = "The ID of the PostgreSQL Flexible Server"
  value       = azurerm_postgresql_flexible_server.postgres.id
}
