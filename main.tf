# Define Resource Group
resource "azurerm_resource_group" "default" {
  name     = "${var.name_prefix}-rg"
  location = var.location
  tags = {
    owner = "tommi.herranen@siili.com"
  }
}

# Generate random password
resource "random_password" "pass" {
  length = 20
}

# Define PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                = "${var.name_prefix}-flexserver"
  resource_group_name = azurerm_resource_group.default.name
  location            = azurerm_resource_group.default.location

  sku_name               = "B_Standard_B1ms" # Change this for production
  storage_mb             = 32768
  version                = "15"
  administrator_login    = "adminuser"
  administrator_password = random_password.pass.result

  backup_retention_days         = 7
  geo_redundant_backup_enabled  = false
  public_network_access_enabled = true # Change to false if using private access

  zone = "1"
}

# Disable SSL enforcement (require_secure_transport = OFF)
resource "azurerm_postgresql_flexible_server_configuration" "disable_ssl" {
  name      = "require_secure_transport"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  value     = "OFF"
}

# Allow Access from Azure Services
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Allow Specific IP Address (Change This)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_local_access" {
  name             = "AllowLocalAccess"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = var.allowed_ip_start
  end_ip_address   = var.allowed_ip_end
}

# Allow Some IP Address (just for testing)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_random_access" {
  name             = "AllowLocalAccess"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = "88.192.119.119"
  end_ip_address   = "88.192.119.119"
}
