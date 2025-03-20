output "storage_account_name" {
  description = "The name of the Storage Account"
  value       = azurerm_storage_account.storage.name
}

output "storage_account_access_key" {
  description = "The access key for the Storage Account"
  value       = azurerm_storage_account.storage.primary_access_key
}

output "storage_account_id" {
  description = "The ID of the Storage Account"
  value       = azurerm_storage_account.storage.id
}
