# App governance

Owners review purpose and access quarterly and when App permissions change, renewing `review_due` by PR. Expiry flags a review; it does not revoke access.

Daily/manual audits report unmanaged or missing installations, all-repository access, missing metadata, and due reviews. Findings or failures update the status issue and fail the workflow. Organization owners investigate unknown Apps before adoption or removal. At scale, teams own and triage their Apps; inventory reads paginate.

Terraform owns complete repository lists. Catalog PRs approve changes, including removing access added manually.

## Removal

1. Confirm consumers and a removal window.
2. Narrow access by PR and check dependent workloads.
3. Uninstall in GitHub settings; revoke credentials you control.
4. Stop applies, back up state, forget that installation's binding, and remove its catalog entry. Review the next plan before resuming.

Deleting an entry alone [leaves one repository accessible](https://github.com/integrations/terraform-provider-github/blob/v6.13.0/github/resource_github_app_installation_repositories.go); it does not uninstall the App.

## Limits

- The tested fine-grained PAT received HTTP 403 on provider installation reads. Classic `repo` + `read:org` worked. Protect this broader credential; privileged plans trust repository collaborators. `workflow` is only needed to publish workflows.
- B2 state is encrypted and private, with a bucket-scoped key. Locking is disabled; CI queues do not coordinate local applies.
- Schedules can run late. Owners must also review App permissions and workload health.
