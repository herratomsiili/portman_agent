output "ai_instrumentation_key" {
  description = "The Instrumentation Key of the Application Insights"
  value       = azurerm_application_insights.app_insights.instrumentation_key
}