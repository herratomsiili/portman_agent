variable "location" {
  description = "Azure region where resources will be deployed"
  type        = string
  #default     = "North Europe"
}

variable "naming_prefix" {
  description = "Prefix for naming all resources"
  type        = string
}

variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string
}

variable "resource_group_owner_tag_value" {
  description = "The value of the mandatory 'Owner' tag for resource group"
  type        = string
}

variable "admin_password" {
  description = "PostgreSQL Admin Password"
  type        = string
  sensitive   = true
}

variable "allowed_ip_start" {
  description = "Allowed ip range start for firewall rule."
  type        = string
}

variable "allowed_ip_end" {
  description = "Allowed ip range end for firewall rule."
  type        = string
}

variable "allowed_ip_local" {
  description = "Allowed local ip for firewall rule."
  type        = string
}

variable "environment" {
  description = "Selected environment."
  type        = string
}

variable "static_web_app_location" {
  description = "Azure Static Web App location"
  type        = string
}