# Allow Access from Azure Services
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = var.postgres_server_id # Use the variable instead of a direct reference
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Allow Specific IP Address (office)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_office_access" {
  name = "AllowOfficeAccess"
  #server_id        = azurerm_postgresql_flexible_server.postgres.id
  server_id        = var.postgres_server_id # Use the variable instead of a direct reference
  start_ip_address = var.allowed_ip_start
  end_ip_address   = var.allowed_ip_end
}

# Allow Specific IP Address (local)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_local_access" {
  name = "AllowLocalAccess"
  #server_id        = azurerm_postgresql_flexible_server.postgres.id
  server_id        = var.postgres_server_id # Use the variable instead of a direct reference
  start_ip_address = var.allowed_ip_local
  end_ip_address   = var.allowed_ip_local
}
