provider "azurerm" {
    features { }
}

resource "azurerm_resource_group" "rg" {
  name     = "ui-engineer-rg"
  location = "East US"
}

resource "azurerm_service_plan" "plan" {
  name                = "ui-engineer-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B2"  # use F1 for free tier
}

resource "azurerm_linux_web_app" "app" {
  name                = "ui-engineer-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      docker_registry_url = "https://index.docker.io"
      docker_image_name = "shroominic/ui-engineer:latest"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "8000"
    "LANGCHAIN_TRACING_V2" = "true"
    "LANGCHAIN_PROJECT" = "ui-engineer"
    "LANGCHAIN_API_KEY" = var.langchain_api_key
    "GROQ_API_KEY" = var.groq_api_key
  }

  public_network_access_enabled = true
  https_only = true
}

variable "groq_api_key" {
  sensitive   = true
}

variable "langchain_api_key" {
  sensitive   = true
}

output "public_ip" {
  value = azurerm_linux_web_app.app.outbound_ip_addresses
  description = "The public IP addresses associated with the app service."
}
