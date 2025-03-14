variable "naming_prefix" {
  description = "Prefix for naming resources"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "admin_password" {
  description = "PostgreSQL Admin Password"
  type        = string
  sensitive   = true
}
