resource "azurerm_static_web_app" "web_ui" {
  name                         = "${var.naming_prefix}-webui"
  resource_group_name          = var.resource_group_name
  location                     = var.static_web_app_location
  sku_tier                     = "Free"
  sku_size                     = "Free"
  preview_environments_enabled = false

  tags = {
    environment = var.environment
    application = "portman-ui"
  }

  # Set app settings for API endpoint
  app_settings = {
    "VITE_API_BASE_URL" = var.dab_api_endpoint
  }
}

resource "azurerm_static_web_app_custom_domain" "api_domain" {
  count             = var.custom_domain != "" ? 1 : 0
  static_web_app_id = azurerm_static_web_app.web_ui.id
  domain_name       = var.custom_domain
  validation_type   = "dns-txt-token"
  depends_on        = [azurerm_static_web_app.web_ui]
}

resource "azurerm_static_web_app_custom_domain" "cert" {
  count             = var.custom_domain != "" ? 1 : 0
  static_web_app_id = azurerm_static_web_app.web_ui.id
  domain_name       = var.custom_domain
  validation_type   = "cname-delegation"
  depends_on        = [azurerm_static_web_app_custom_domain.api_domain[0]]
}

# Output variables for use in GitHub Actions
output "deployment_token" {
  value     = azurerm_static_web_app.web_ui.api_key
  sensitive = true
}

output "static_website_url" {
  value = azurerm_static_web_app.web_ui.default_host_name
} 