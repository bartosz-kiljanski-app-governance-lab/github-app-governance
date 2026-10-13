bucket               = "devops-github-assignment"
region               = "eu-central-003"
key                  = "github-app-governance/bartosz-kiljanski-app-governance-lab/terraform.tfstate"
workspace_key_prefix = "github-app-governance/bartosz-kiljanski-app-governance-lab/workspaces"

endpoints = {
  s3 = "https://s3.eu-central-003.backblazeb2.com"
}

encrypt                     = true
use_lockfile                = false
use_path_style              = true
skip_credentials_validation = true
skip_metadata_api_check     = true
skip_region_validation      = true
skip_requesting_account_id  = true
