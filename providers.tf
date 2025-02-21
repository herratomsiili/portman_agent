terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "therranen-portman-rg"
    storage_account_name = "therranenportmanstorage"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    #use_oidc             = true # Enables OpenID Connect authentication
  }
}

provider "azurerm" {
  features {}
}