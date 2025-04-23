module "common" {
  source = "../common"

  naming_prefix                  = var.naming_prefix
  location                       = var.location
  resource_group_owner_tag_value = var.resource_group_owner_tag_value
  allowed_ip_start               = var.allowed_ip_start
  allowed_ip_end                 = var.allowed_ip_end
  allowed_ip_local               = var.allowed_ip_local
  admin_password                 = var.admin_password
  storage_account_name           = var.storage_account_name
  environment                    = var.environment
  static_web_app_location        = var.static_web_app_location
}

output "admin_username" {
  value = module.common.admin_username
}

output "admin_password" {
  value     = module.common.admin_password
  sensitive = true
}

output "postgresql_fqdn" {
  value = module.common.postgresql_fqdn
}

output "dab_container_app_url" {
  value = module.common.dab_container_app_url
}

output "static_website_url" {
  value = module.common.static_website_url
}

output "webui_deployment_token" {
  value     = module.common.webui_deployment_token
  sensitive = true
}
