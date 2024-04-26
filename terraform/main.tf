provider "azurerm" {
    features { }
}

resource "azurerm_resource_group" "rg" {
  name     = "ui-engineer-rg"
  location = "UK South"
}

// CONTAINER APP

resource "azurerm_service_plan" "plan" {
  name                = "ui-engineer-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "P1v2"
}

resource "azurerm_linux_web_app" "app" {
  name                = "ui-engineer-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id
  public_network_access_enabled = true
  https_only = true

  site_config {
    application_stack {
      docker_registry_url = "https://index.docker.io"
      docker_image_name = "shroominic/ui-engineer:latest"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "8000"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "LANGCHAIN_TRACING_V2" = "true"
    "LANGCHAIN_PROJECT" = "ui-engineer"
    "LANGCHAIN_API_KEY" = var.langchain_api_key
    "GROQ_API_KEY" = var.groq_api_key
  }
}

// VARIABLES

variable "groq_api_key" {
  type        = string
  sensitive   = true
}

variable "langchain_api_key" {
  type        = string
  sensitive   = true
}

output "public_ip" {
  value = azurerm_linux_web_app.app.outbound_ip_addresses
  description = "The public IP addresses associated with the app service."
}
