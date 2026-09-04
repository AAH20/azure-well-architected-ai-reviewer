targetScope = 'subscription'

@description('Azure Developer CLI environment name.')
param environmentName string

@description('Deployment region.')
param location string = deployment().location

@description('Provision an Azure Container Apps environment for a future hosted API. Disabled by default to minimize cost.')
param deployHostedRuntime bool = false

var suffix = uniqueString(subscription().id, environmentName)
var resourceGroupName = 'rg-architecture-reviewer-${environmentName}'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: {
    solution: 'azure-well-architected-ai-reviewer'
    environment: environmentName
    managedBy: 'azd-bicep'
    evidenceStatus: 'requires-post-deployment-verification'
  }
}

module observability 'observability.bicep' = {
  name: 'observability-${suffix}'
  scope: resourceGroup
  params: {
    location: location
    environmentName: environmentName
    suffix: suffix
    deployHostedRuntime: deployHostedRuntime
  }
}

output AZURE_RESOURCE_GROUP string = resourceGroup.name
output AZURE_LOG_ANALYTICS_WORKSPACE_ID string = observability.outputs.workspaceId
