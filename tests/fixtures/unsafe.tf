resource "azurerm_storage_account" "unsafe" {
  name                          = "unsafe"
  public_network_access_enabled = true
  allow_blob_public_access      = true
  min_tls_version               = "TLS1_0"
}

resource "azurerm_kubernetes_cluster_node_pool" "production" {
  node_count = 1 # production
}
