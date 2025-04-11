output "openai_endpoint" {
  description = "The endpoint of the OpenAI account"
  value       = azurerm_cognitive_account.openai.endpoint
}

output "openai_id" {
  description = "The ID of the OpenAI account"
  value       = azurerm_cognitive_account.openai.id
}

output "openai_primary_key" {
  description = "The primary key of the OpenAI account"
  value       = azurerm_cognitive_account.openai.primary_access_key
  sensitive   = true
}

output "deployment_id" {
  description = "The ID of the deployment"
  value       = azurerm_cognitive_deployment.deployment.id
}

output "deployment_name" {
  description = "The name of the deployment"
  value       = azurerm_cognitive_deployment.deployment.name
} 