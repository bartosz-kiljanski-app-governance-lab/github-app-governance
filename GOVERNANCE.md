# App governance

Each installation has an accountable owner, purpose, review deadline, and allowed repository list in `config/apps.yaml`. App registration and installation are bootstrap steps; this repository governs access to existing installations.

Owners review access at least quarterly and whenever an App's purpose or requested permissions change. They confirm the repository list and renew `review_due` through a PR. That date expires the recorded approval, not the live installation. Due reviews need an owner decision; automatic deletion could break builds or deployments.

## Detection and changes

The audit compares the organization's live installation IDs with the catalog daily and on manual runs. It reports unmanaged Apps, missing installations, all-repository access, incomplete ownership metadata, and due reviews. Findings fail the audit and appear in its logs, summary, and configured status issue; failures replace any old clean status. It never modifies App access. The workflow's built-in token updates the issue with `issues: write`.

For an unmanaged App, an organization owner identifies its installer and consumers, then adopts it with an owner and matching access or schedules removal. For hundreds of Apps, assign owners to teams and have them triage their findings; the audit paginates the inventory. This demo does not build a separate ticketing integration.

Normal changes edit the catalog, review the PR plan, and merge for apply. Terraform owns each managed installation's complete repository list. Check unexpected removals carefully: access added outside the catalog is not an approved exception.

## Decommissioning

1. Confirm consumers and a removal window with the App and repository owners.
2. Narrow access through a PR and check dependent builds and webhooks.
3. An organization owner uninstalls the App in GitHub settings; revoke any associated credentials you control.
4. With applies stopped, back up state, forget only that installation's Terraform binding, and remove its catalog entry. Resume applies after a reviewed plan confirms no unrelated changes.

Deleting a catalog entry alone is unsafe: the pinned provider's [delete implementation](https://github.com/integrations/terraform-provider-github/blob/v6.13.0/github/resource_github_app_installation_repositories.go) leaves one repository accessible. It does not uninstall the App.

## Security limits

- The tested fine-grained PAT could read repository metadata but received HTTP 403 from the provider's installation-repository read endpoint. A classic PAT with `repo` and `read:org` worked for reads and access changes. It is broader than ideal; restrict its owner, lifetime, and storage. `workflow` is needed only to publish workflow files.
- Credentialed PR jobs trust collaborators who can push branches in this repository. Fork jobs are skipped. Review Terraform, scripts, workflows, and provider updates as code that can use those credentials.
- B2 stores encrypted state in a private bucket using a bucket-scoped key. Locking is disabled; the Actions queue serializes CI jobs, but does not coordinate local applies or other repositories. Stop CI writes before local maintenance.
- Scheduled audit runs can be delayed. App permission changes and workload health need owner review; repository access alone does not prove an App is safe.
