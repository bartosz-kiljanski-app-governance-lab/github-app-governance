# GitHub App governance

`config/apps.yaml` records owners, purpose, review dates, installation IDs, and allowed repositories. Terraform owns each installation's complete repository list. Catalog PRs get a plan comment; merging to main applies the change.

Terraform also protects main: PRs, its GitHub Actions check, and resolved conversations are required, including for admins. This single-owner demo requires zero approving reviews.

## Run in your organization

Use Terraform 1.16.x. Existing repositories and selected-access App installations are required.

1. Clone into a fresh directory. Edit `config/apps.yaml` to match your organization and current access.
2. Edit `config/backend.hcl` for your bucket, endpoint, region, and a dedicated state key. B2 and AWS S3 examples are in `config/`.
3. Set credentials outside Git: `GITHUB_TOKEN` (organization-owner classic PAT with `repo` and `read:org`), `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY`. For B2, these are its application key ID and key.
4. If your governance repository has a different name, set `TF_VAR_governance_repository`.

```powershell
cd terraform
terraform init -lockfile=readonly '-backend-config=../config/backend.hcl'
terraform plan '-out=adoption.tfplan'
terraform apply 'adoption.tfplan'
terraform plan -detailed-exitcode
```

Review the saved plan before applying. Initial adoption imports the Apps without access changes and creates main protection. If main is already protected, import it before planning:

```powershell
terraform import github_branch_protection_v3.main 'YOUR-REPOSITORY:main'
```

Imports are skipped once recorded in your state. Plan exit codes: `0` unchanged, `2` changes, `1` error.

## Actions and audit

Configure secrets `GOVERNANCE_GITHUB_TOKEN`, `STATE_ACCESS_KEY_ID`, and `STATE_SECRET_ACCESS_KEY`; optionally `STATE_SESSION_TOKEN`. Actions uses its own repository name. Fork PRs fail before checkout. Manual Terraform runs only plan.

**Audit GitHub Apps** runs daily or manually and reports unmanaged installations and due reviews without changing access. Create and pin a status issue, then set `AUDIT_STATUS_ISSUE_NUMBER`; each audit replaces its body.

Locally, from the repository root: `python -m pip install -r requirements.txt`, then `python scripts/audit_apps.py`. Audit exits: `0` clean, `1` findings, `2` error.

This deployment uses B2 without state locking. CI serializes Terraform jobs; avoid concurrent local applies. Never commit credentials, state, or plans. See [GOVERNANCE.md](GOVERNANCE.md) for reviews, removal, and limits.
