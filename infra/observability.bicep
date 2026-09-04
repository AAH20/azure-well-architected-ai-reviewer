param location string
param environmentName string
param suffix string
param deployHostedRuntime bool

resource workspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-architecture-reviewer-${environmentName}-${suffix}'
  location: location
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
  tags: {
    environment: environmentName
  }
}

resource hostedEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = if (deployHostedRuntime) {
  name: 'cae-architecture-reviewer-${environmentName}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: workspace.properties.customerId
        sharedKey: workspace.listKeys().primarySharedKey
      }
    }
  }
}

output workspaceId string = workspace.id
output hostedEnvironmentId string = deployHostedRuntime ? hostedEnvironment!.id : ''
