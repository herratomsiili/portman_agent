terraform {
  #backend "azurerm" {
  #  resource_group_name  = "therranen-portman-rgxx"
  #  storage_account_name = "therranenportmanstorage"
  #  container_name       = "tfstate"
  #  #key                  = "development.tfstate"
  #  key = "terraform.tfstate"
  #  #use_oidc             = true
  #}
  backend "azurerm" {}
}
