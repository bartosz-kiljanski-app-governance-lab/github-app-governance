data "github_app" "github_actions" {
  slug = "github-actions"
}

resource "github_branch_protection_v3" "main" {
  repository                      = var.governance_repository
  branch                          = "main"
  enforce_admins                  = true
  require_conversation_resolution = true

  required_status_checks {
    strict = true
    checks = ["terraform:${data.github_app.github_actions.id}"]
  }

  required_pull_request_reviews {
    required_approving_review_count = 0
  }
}
