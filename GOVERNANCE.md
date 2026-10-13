# App governance

Owners review purpose and access quarterly and when App permissions change, renewing `review_due` by PR. Expiry flags review; it does not revoke access.

Daily/manual audits report unmanaged or missing installations, all-repository access, missing metadata, and due reviews. Findings or errors fail the workflow and update the status issue. Inventory reads paginate.

For hundreds of Apps, use team ownership and require CODEOWNERS review of catalog changes (not enabled in this demo). The platform team investigates unknown Apps before adoption or removal and escalates overdue reviews to owners.

Terraform owns complete repository lists, including access added manually.

## Removal

1. Confirm consumers and a removal window.
2. Narrow access by PR; check dependent workloads.
3. Pause new applies, wait for running applies to finish, and back up state.
4. Uninstall in GitHub settings; revoke credentials you control.
5. Forget that installation's binding and remove its catalog entry. Review before resuming.

Deleting an entry alone [leaves one repository accessible](https://github.com/integrations/terraform-provider-github/blob/v6.13.0/github/resource_github_app_installation_repositories.go); it does not uninstall the App.

## Limits

- The tested fine-grained PAT received HTTP 403 on installation reads. Classic `repo` + `read:org` worked. Fine-grained support is [documented](https://docs.github.com/en/rest/apps/installations#add-a-repository-to-an-app-installation); verify provider operations before switching. Protect this broader credential; plans trust repository collaborators. `workflow` is only needed for publishing workflows.
- B2 state is encrypted and private with a bucket-scoped key. CI queues do not coordinate local applies.
- Schedules can run late. Owners must also review App permissions and workload health.
