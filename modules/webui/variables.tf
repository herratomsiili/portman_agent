variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure region where resources should be created"
  type        = string
}

variable "naming_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "environment" {
  description = "The environment (development, testing, production)"
  type        = string
  #default     = "development"
}

variable "custom_domain" {
  description = "Custom domain for the static web app (optional)"
  type        = string
  default     = ""
}

variable "dab_api_endpoint" {
  description = "The DAB API endpoint to connect to"
  type        = string
  default     = ""
}

variable "static_web_app_location" {
  description = "Azure Static Web App location"
  type        = string
} 