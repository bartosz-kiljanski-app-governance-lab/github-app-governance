# github-app-governance

Terraform manages repository access for existing GitHub App installations.

`config/apps.yaml` records each App's owner, purpose, review date, installation ID, and allowed repositories. Terraform manages the complete repository list for each installation. Access changes start with a catalog edit and a reviewed plan. Review dates do not automatically revoke access.

## Run in your organization

Use Terraform 1.16.x and the pinned GitHub provider 6.13.0. Repositories and selected-access App installations must already exist.

1. Clone this repository into a new directory to start with empty state. Do not reuse another organization's state.
2. Replace the organization, App details, installation IDs, and repository names in `config/apps.yaml`. For initial adoption, match the live repository lists.
3. Copy the appropriate backend example to `config/backend.tfbackend`: `backend.tfbackend.example` for AWS S3, or `backend.b2.tfbackend.example` for B2. Set your bucket, region, and a state key dedicated to your organization.
4. Set `GITHUB_TOKEN` securely using a classic PAT with `repo` and `read:org`, belonging to an organization owner with repository administration access. Supply storage credentials through `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (B2 key ID/application key for B2, AWS credentials for S3).

```powershell
terraform init -input=false -lockfile=readonly '-backend-config=config/backend.tfbackend'
terraform fmt -check
terraform validate
terraform plan -input=false -detailed-exitcode '-out=adoption.tfplan'
```

The import block adopts the catalog's installations into your new state. With matching repository lists, the first plan proposes imports without access changes. Review it before applying.

```powershell
terraform apply -input=false 'adoption.tfplan'
terraform plan -input=false -detailed-exitcode
```

Plan exit codes: `0` no changes, `2` proposed changes, `1` error.

After adoption, imports are skipped for resources already in state. Further access changes come from editing the catalog.

This deployment uses B2; reviewers can configure AWS S3 or another S3-compatible backend. B2 state locking is disabled; run only one apply at a time. Never commit credentials, state, saved plans, or your configured backend file.

Removing an App entry does not uninstall it; provider deletion leaves one repository accessible.
