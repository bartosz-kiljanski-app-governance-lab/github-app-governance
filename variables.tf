variable "github_owner" {
  description = "GitHub organization containing the existing App installation and repository."
  type        = string
}

variable "app_a_installation_id" {
  description = "App A's organization installation ID, not its App registration ID."
  type        = string
}

variable "app_a_repository" {
  description = "Short name of the existing repository App A can access."
  type        = string
}

variable "app_a_temporary_repository" {
  description = "Short name of the existing repository temporarily granted to App A for Phase 1."
  type        = string
}
