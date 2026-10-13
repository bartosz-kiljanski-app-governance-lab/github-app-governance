variable "apps_catalog_path" {
  description = "Path to the GitHub App access catalog, relative to the Terraform root or absolute."
  type        = string
  default     = "../config/apps.yaml"
}

variable "governance_repository" {
  description = "Existing repository whose main branch requires Terraform checks and pull requests."
  type        = string
  default     = "github-app-governance"
}
