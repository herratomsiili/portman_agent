#resource "azurerm_service_plan" "dab_plan" {
#  name                = "${var.naming_prefix}-dab-asp"
#  resource_group_name = var.resource_group_name
#  location            = var.location
#  os_type             = "Linux"
#  sku_name            = "B1"
#}

#resource "azurerm_storage_container" "dab_config" {
#  name                  = var.config_container_name
#  storage_account_name  = var.storage_account_name
#  container_access_type = "private"
#}

#resource "azurerm_storage_blob" "dab_config_json" {
#  name                   = "dab-config.json"
#  storage_account_name   = var.storage_account_name
#  storage_container_name = azurerm_storage_container.dab_config.name
#  type                   = "Block"
#  source                 = "${path.module}/dab-config.json" # Uploads local `dab-config.json`
#}

# Create an Azure Storage Share for the DAB config
resource "azurerm_storage_share" "dab_config_share" {
  name                 = "dab-config-files"
  storage_account_name = var.storage_account_name
  quota                = 5 # 5 GB storage
}

# Upload the `dab-config.json` file to the Azure File Share
resource "azurerm_storage_share_file" "dab_config_json" {
  name             = "dab-config.json"
  storage_share_id = azurerm_storage_share.dab_config_share.id
  source           = "${path.module}/dab-config.json" # Ensure file exists locally
}

#resource "azurerm_linux_web_app" "dab_app" {
#  name                = "${var.naming_prefix}-dab-app"
#  resource_group_name = var.resource_group_name
#  location            = var.location
#  service_plan_id     = azurerm_service_plan.dab_plan.id
#
#  site_config {
#    always_on     = true
#    ftps_state    = "Disabled"
#    http2_enabled = true
#    application_stack {
#      docker_registry_url = "https://mcr.microsoft.com"
#      docker_image_name   = "azure-databases/data-api-builder:latest"
#    }
#  }
#
#  storage_account {
#    account_name = var.storage_account_name
#    name         = "dab-config"
#    type         = "AzureFiles"
#    share_name   = azurerm_storage_share.dab_config_share.name
#    access_key   = var.storage_account_access_key
#    mount_path   = "/App/dab-config" # Ensures App Service can access the file
#  }
#
#  app_settings = {
#    "DAB_ENVIRONMENT"                     = "Development"
#    "DATABASE_CONNECTION_STRING"          = var.database_connection_string
#    "DAB_CONFIG_PATH"                     = "/App/dab-config/dab-config.json"
#    "DAB_PORT"                            = "80"
#    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "true"
#    #"DAB_CONFIG_STORAGE_ACCOUNT"     = var.storage_account_name
#    #"DAB_CONFIG_CONTAINER_NAME"      = azurerm_storage_container.dab_config.name
#    #"DAB_CONFIG_BLOB_NAME"           = azurerm_storage_blob.dab_config_json.name
#    "APPINSIGHTS_INSTRUMENTATIONKEY" = var.ai_instrumentation_key
#  }
#}

resource "azurerm_container_app_environment" "dab_env" {
  name                = "${var.naming_prefix}-dap-cont-env"
  resource_group_name = var.resource_group_name
  location            = var.location
}

# Register Storage Inside the Container Apps Environment
resource "azurerm_container_app_environment_storage" "dab_storage" {
  name                         = "dab-config-storage"
  container_app_environment_id = azurerm_container_app_environment.dab_env.id
  account_name                 = var.storage_account_name
  share_name                   = azurerm_storage_share.dab_config_share.name
  access_key                   = var.storage_account_access_key
  access_mode                  = "ReadOnly"
}

resource "azurerm_container_app" "dab_cont" {
  name                = "${var.naming_prefix}-dab-cont"
  resource_group_name = var.resource_group_name
  #location                     = var.location
  container_app_environment_id = azurerm_container_app_environment.dab_env.id

  revision_mode = "Single"

  ingress {
    external_enabled = true # Accept traffic from anywhere
    target_port      = 5000 # Ensure port 5000 is exposed
    #transport        = "http"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    container {
      name   = "dab"
      image  = "mcr.microsoft.com/azure-databases/data-api-builder:0.11.132"
      cpu    = "0.5" # Minimum: 0.25, Recommended: 0.5 or 1.0
      memory = "1Gi" # Minimum: 0.5Gi, Recommended: 1Gi or more

      args = ["--ConfigFileName=./dab-config/dab-config.json"]

      env {
        name  = "DATABASE_CONNECTION_STRING"
        value = var.database_connection_string
      }

      env {
        name  = "DAB_ENVIRONMENT"
        value = "Development"
      }

      volume_mounts {
        name = "config-volume"
        path = "/App/dab-config"
      }
    }

    volume {
      name         = "config-volume"
      storage_name = azurerm_container_app_environment_storage.dab_storage.name
      storage_type = "AzureFile"
    }
  }
}
