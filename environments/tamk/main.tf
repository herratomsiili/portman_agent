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

# Load environment-specific variables
variable "environment" {
  default = "tamk"
}
