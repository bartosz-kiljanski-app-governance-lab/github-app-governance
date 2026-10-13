variable "apps_catalog_path" {
  description = "Path to the GitHub App access catalog, relative to the Terraform root or absolute."
  type        = string
  default     = "config/apps.yaml"
}
