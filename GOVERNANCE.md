# App governance

Owners review purpose and repository access quarterly and when App permissions change, renewing `review_due` through a PR. Expiry flags a review; it does not revoke access.

The daily/manual audit reports unmanaged or missing installations, all-repository access, missing ownership metadata, and due reviews. Findings and failures update the pinned issue and fail the workflow. No access is removed automatically. Organization owners adopt or remove unknown Apps; at scale, teams triage their Apps using the paginated inventory.

Access changes go through catalog PRs. Terraform owns each installation's complete repository list, including removing access added manually.

## Removal

1. Confirm consumers and a removal window.
2. Narrow access through a PR; check dependent workloads.
3. Uninstall in GitHub settings and revoke credentials you control.
4. Stop applies, back up state, forget that installation's binding, and remove its catalog entry. Review the next plan before resuming.

Deleting a catalog entry alone [leaves one repository accessible](https://github.com/integrations/terraform-provider-github/blob/v6.13.0/github/resource_github_app_installation_repositories.go); it does not uninstall the App.

## Limits

- The tested fine-grained PAT received HTTP 403 on provider installation reads. Classic `repo` + `read:org` worked; protect this broader credential. `workflow` is only needed for publishing workflows. Credentialed plans trust repository collaborators.
- B2 state is encrypted in a private bucket with a bucket-scoped key. Locking is disabled. CI queues do not coordinate local applies; stop CI writes before maintenance.
- Scheduled audits can run late. Owners must also review App permissions and workload health.
