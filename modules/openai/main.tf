resource "azurerm_cognitive_account" "openai" {
  name                = "${var.naming_prefix}-openai"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "OpenAI"
  sku_name            = var.sku_name

  custom_subdomain_name         = lower("${var.naming_prefix}-openai")
  public_network_access_enabled = var.public_network_access_enabled
}

resource "azurerm_cognitive_deployment" "deployment" {
  name                 = var.deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id
  model {
    format  = "OpenAI"
    name    = var.model_name
    version = var.model_version
  }

  scale {
    type     = "Standard"
    capacity = var.deployment_capacity
  }
} 