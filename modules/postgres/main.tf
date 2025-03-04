# Define Resource Group
#resource "azurerm_resource_group" "default" {
#  name     = var.resource_group_name
#  location = var.location
#  tags = {
#    owner = "tommi.herranen@siili.com"
#  }
#}

# Define PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                = var.postgres_name
  resource_group_name = var.resource_group_name
  location            = var.location

  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  version                = "15"
  administrator_login    = "adminuser"
  administrator_password = var.admin_password

  backup_retention_days         = 7
  geo_redundant_backup_enabled  = false
  public_network_access_enabled = true

  zone = "1"
}

# Disable SSL enforcement (require_secure_transport = OFF)
resource "azurerm_postgresql_flexible_server_configuration" "disable_ssl" {
  name      = "require_secure_transport"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  value     = "OFF"
}