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
  resource_group_name = var.resource_group_name
  location            = var.location
  postgres_name       = "${var.naming_prefix}-flexserver"
  admin_password      = var.admin_password
}