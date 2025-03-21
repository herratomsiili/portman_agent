variable "resource_group_name" {
  description = "Resource group for deployment"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "naming_prefix" {
  description = "Prefix for naming resources"
  type        = string
}

variable "storage_account_name" {
  description = "Storage account for config.json"
  type        = string
}

variable "storage_account_access_key" {
  description = "Storage account access key"
  type        = string
}

variable "storage_account_id" {
  description = "Storage account ID"
  type        = string
}

#variable "config_container_name" {
#  description = "Blob container for config.json"
#  type        = string
#  default     = "dab-config"
#}

variable "database_connection_string" {
  description = "PostgreSQL connection string for DAB"
  type        = string
}

variable "ai_instrumentation_key" {
  description = "Instrumentation key of the Application Insights resource"
  type        = string
}