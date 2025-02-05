# Setting up workload identity federation for github actions

# Allowed GitHub repos to use the workload identity federation service account
locals {
  # Place the allowed repo in alphabetical order 
  allowed_repos = [
    "akhileshmishra/repos-names",
    "orgname/reponame"
  ]

  allowed_subjects = flatten([
    # For main branch
    [for repo in local.allowed_repos : "repo:${repo}:ref:refs/heads/main"],
    # For pull requests
    [for repo in local.allowed_repos : "repo:${repo}:pull_request"]
  ])

}

# These resources are imported from gcp to harden the security and strictly allow particular 
# Repos under KPMG-UK org
resource "google_iam_workload_identity_pool" "main" {
  description               = "workload-pool"
  disabled                  = false
  display_name              = "workload-pool"
  project                   = var.project_id
  workload_identity_pool_id = var.workload_identity_pool_id
}

resource "google_iam_workload_identity_pool_provider" "main" {
  # attribute_condition = "assertion.repository_owner=='orgname' && assertion.repository in ${jsonencode(local.allowed_repos)}"
  attribute_condition = "assertion.sub in ${jsonencode(local.allowed_subjects)}"

  attribute_mapping = {
    "attribute.actor"      = "assertion.actor"
    "attribute.aud"        = "assertion.aud"
    "attribute.repository" = "assertion.repository"
    "google.subject"       = "assertion.sub"
  }
  description                        = "Workload Identity Pool Provider"
  disabled                           = false
  display_name                       = "github"
  project                            = var.project_id
  workload_identity_pool_id          = var.workload_identity_pool_id
  workload_identity_pool_provider_id = var.google_iam_workload_identity_pool_provider
  oidc {
    allowed_audiences = []
    issuer_uri        = "https://token.actions.githubusercontent.com"
    jwks_json         = null
  }
}
