# Output Database Connection Details
output "postgresql_fqdn" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

#output "database_name" {
#  value = azurerm_postgresql_flexible_server_database.db.name
#}

output "admin_username" {
  value     = azurerm_postgresql_flexible_server.postgres.administrator_login
  sensitive = true
}

output "admin_password" {
  value     = azurerm_postgresql_flexible_server.postgres.administrator_password
  sensitive = true
}
