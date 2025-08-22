targetScope = 'subscription'

@description('Azure region for all resources')
param location string

@description('Environment name, used for resource naming and tagging')
param environmentName string

@description('Resource group name to create')
param resourceGroupName string

// Token used for resource naming uniqueness at subscription scope
var resourceToken = uniqueString(subscription().id, location, environmentName)
// Three-letter resource prefix per guidance
var resourcePrefix = 'hda'

// Create resource group with required tag
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: {
    'azd-env-name': environmentName
  }
}

module resources 'resources.bicep' = {
  name: 'rg-resources'
  scope: rg
  params: {
    location: location
    environmentName: environmentName
    resourceToken: resourceToken
    resourcePrefix: resourcePrefix
  }
}

output RESOURCE_GROUP_ID string = rg.id
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
