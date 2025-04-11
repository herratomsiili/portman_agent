resource "azurerm_resource_group" "main" {
  name     = "${var.naming_prefix}-rg"
  location = var.location
  tags = {
    owner = var.resource_group_owner_tag_value
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
  postgresql_fqdn        = module.postgres.postgresql_fqdn
  admin_username         = module.postgres.admin_username
  admin_password         = module.postgres.admin_password
}

module "monitoring" {
  source              = "../../modules/monitoring"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  naming_prefix       = var.naming_prefix
}

module "dab_service" {
  source                     = "../../modules/dab_service"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = var.location
  naming_prefix              = var.naming_prefix
  storage_account_name       = module.appservice.storage_account_name
  storage_account_access_key = module.appservice.storage_account_access_key
  storage_account_id         = module.appservice.storage_account_id
  ai_instrumentation_key     = module.monitoring.ai_instrumentation_key
  database_connection_string = "Host=${module.postgres.postgresql_fqdn};Port=5432;Database=portman;Username=${module.postgres.admin_username};Password=${module.postgres.admin_password}"
}

module "openai" {
  source              = "../../modules/openai"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  naming_prefix       = var.naming_prefix
  deployment_capacity = 5

  tags = {
    environment = var.environment
    application = "portman-cargo-generator"
  }
} 