# Adopt this existing relationship with terraform import before applying.
resource "github_app_installation_repository" "app_a_baseline" {
  installation_id = var.app_a_installation_id
  repository      = var.app_a_repository
}

# Test to check if grants work. Remove to restore baseline
resource "github_app_installation_repository" "app_a_temporary" {
  installation_id = var.app_a_installation_id
  repository      = var.app_a_temporary_repository
}
