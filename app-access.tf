locals {
  catalog = yamldecode(file(var.apps_catalog_path))
  apps    = local.catalog.apps

  organization_installations = {
    for installation in data.github_organization_app_installations.current.installations :
    tostring(installation.id) => installation.repository_selection
  }
}

data "github_organization_app_installations" "current" {
  lifecycle {
    precondition {
      condition     = length(distinct([for app in values(local.apps) : tostring(app.installation_id)])) == length(local.apps)
      error_message = "Each installation ID must occur only once in the catalog."
    }

    postcondition {
      condition     = lower(self.id) == lower(local.catalog.organization)
      error_message = "The effective GitHub owner differs from the catalog organization. Unset GITHUB_OWNER and GITHUB_ORGANIZATION."
    }
  }
}

resource "github_app_installation_repositories" "apps" {
  for_each = local.apps

  installation_id       = tostring(each.value.installation_id)
  selected_repositories = toset(each.value.repositories)

  lifecycle {
    precondition {
      condition     = length(each.value.repositories) > 0
      error_message = "${each.key}: repositories must not be empty."
    }

    precondition {
      condition     = lookup(local.organization_installations, tostring(each.value.installation_id), "") == "selected"
      error_message = "${each.key}: the installation must exist in the configured organization and use selected repository access."
    }
  }
}
