resource "azurerm_resource_group" "main" {
  name     = "${var.naming_prefix}-rg"
  location = var.location
  tags = {
    owner = "tommi.herranen@siili.com"
  }
}

module "networking" {
  source           = "../../modules/networking"
  allowed_ip_start = var.allowed_ip_start
  allowed_ip_end   = var.allowed_ip_end
  allowed_ip_local = var.allowed_ip_local
  #resource_group_name = var.resource_group_name
  #vnet_name           = "${var.naming_prefix}-vnet"
  #location            = var.location

  postgres_server_id = module.postgres.postgres_server_id # Pass server ID from "postgres" module
}

module "postgres" {
  source              = "../../modules/postgres"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  naming_prefix       = var.naming_prefix
  admin_password      = var.admin_password
}

module "appservice" {
  source                 = "../../modules/appservice"
  resource_group_name    = azurerm_resource_group.main.name
  location               = var.location
  naming_prefix          = var.naming_prefix
  storage_account_name   = var.storage_account_name
  ai_instrumentation_key = module.monitoring.ai_instrumentation_key
}

module "monitoring" {
  source              = "../../modules/monitoring"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  naming_prefix       = var.naming_prefix
}