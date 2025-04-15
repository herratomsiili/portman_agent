variable "naming_prefix" {
  description = "Prefix for naming resources"
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "sku_name" {
  description = "The SKU name for the OpenAI account"
  type        = string
  default     = "S0"
}

variable "tags" {
  description = "Tags to apply to the resources"
  type        = map(string)
  default     = {}
}

variable "public_network_access_enabled" {
  description = "Whether public network access is enabled"
  type        = bool
  default     = true
}

variable "deployment_name" {
  description = "The name of the model deployment"
  type        = string
  default     = "cargo-generator"
}

variable "model_name" {
  description = "The name of the model to deploy"
  type        = string
  default     = "gpt-4o"
}

variable "model_version" {
  description = "The version of the model to deploy"
  type        = string
  default     = "2024-11-20"
}

variable "deployment_capacity" {
  description = "The capacity of the deployment"
  type        = number
  default     = 1
} 