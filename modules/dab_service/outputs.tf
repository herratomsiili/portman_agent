output "dab_container_app_url" {
  description = "The public URL of the Azure Container App"
  value       = "https://${azurerm_container_app.dab_cont.latest_revision_fqdn}"
}
