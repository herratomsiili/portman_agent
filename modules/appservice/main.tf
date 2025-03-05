resource "azurerm_service_plan" "function_plan" {
  name                = "${var.naming_prefix}-asp"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_function_app" "function_app" {
  name                       = "${var.naming_prefix}-func"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  app_service_plan_id        = azurerm_service_plan.function_plan.id
  os_type                    = "linux"
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = var.ai_instrumentation_key
  }
}
