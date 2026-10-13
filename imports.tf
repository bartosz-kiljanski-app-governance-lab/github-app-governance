import {
  for_each = local.apps
  to       = github_app_installation_repositories.apps[each.key]
  id       = tostring(each.value.installation_id)
}
