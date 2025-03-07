terraform {
  backend "azurerm" {
    resource_group_name  = "therranen-portman-rg"
    storage_account_name = "therranenportmanstorage"
    container_name       = "tfstate"
    key                  = "development.tfstate"
  }
}
