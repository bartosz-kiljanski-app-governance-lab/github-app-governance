# GitHub App governance

`config/apps.yaml` records ownership, purpose, review dates, installation IDs, and allowed repositories. Terraform owns each installation's complete repository list. PRs show the plan; merging to main applies it.

Terraform protects main with required PRs, its Actions check, and resolved conversations, including for admins. Required approvals are zero for this single-owner demo.

## Verified demonstration

- [Access narrowing PR and plan comment](https://github.com/bartosz-kiljanski-app-governance-lab/github-app-governance/pull/10)
- [Successful merge/apply](https://github.com/bartosz-kiljanski-app-governance-lab/github-app-governance/actions/runs/38452867268)
- [Successful audit](https://github.com/bartosz-kiljanski-app-governance-lab/github-app-governance/actions/runs/38455324892)

## Reviewer setup

Use Terraform 1.16.x and existing selected-access App installations. Branch protection requires a public repository or a [plan supporting private-repository protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

1. Clone into a fresh directory. Edit `config/apps.yaml` to match your organization, installations, and current repository access.
2. Edit `config/backend.hcl` for your bucket and a dedicated state key. B2 and AWS S3 examples are in `config/`.
3. As an organization owner, create an expiring [classic PAT](https://github.com/settings/tokens) with `repo` + `read:org`; set `GITHUB_TOKEN` outside Git. Set `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` using your state credentials (B2: application key ID/key).
4. For a different governance repository name, set `TF_VAR_governance_repository`.

```powershell
cd terraform
terraform init -lockfile=readonly '-backend-config=../config/backend.hcl'
```

For local reviewer runs, skip backend configuration and state credentials, remove `terraform/backend.tf`, and run `terraform init -lockfile=readonly` from `terraform/`. CI needs shared remote state; other backends require updating `backend.tf` and workflow initialization/credentials.

If main already has protection, adopt it first:

```powershell
terraform import github_branch_protection_v3.main 'YOUR-REPOSITORY:main'
```

```powershell
terraform plan '-out=adoption.tfplan'
```

Review before applying. Matching App access produces imports without access changes; main protection is created if needed.

```powershell
terraform apply 'adoption.tfplan'
terraform plan -detailed-exitcode
```

Imports are skipped afterward. Plan exits: `0` unchanged, `2` changes, `1` error.

## Actions and audit

In repository Settings → Secrets and variables → Actions, save your PAT as `GOVERNANCE_GITHUB_TOKEN` and state credentials as `STATE_ACCESS_KEY_ID`, `STATE_SECRET_ACCESS_KEY` (optionally `STATE_SESSION_TOKEN`). Actions protects the repository running the workflow. Fork PRs fail before checkout; manual Terraform runs only plan.

**Audit GitHub Apps** runs daily or manually without changing access. Pin an issue and set `AUDIT_STATUS_ISSUE_NUMBER` to receive its latest report.

From the repository root, run `python -m pip install -r requirements.txt`, then `python scripts/audit_apps.py`. Audit exits: `0` clean, `1` findings, `2` error.

B2 locking is disabled. CI serializes Terraform jobs; avoid concurrent local applies. Never commit credentials, state, or plans. See [GOVERNANCE.md](GOVERNANCE.md) for reviews, removal, and limits.
