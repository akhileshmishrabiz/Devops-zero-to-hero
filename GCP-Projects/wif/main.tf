# Setting up workload identity federation for github actions

# Allowed GitHub repos to use the workload identity federation service account
locals {
  # Place the allowed repo in alphabetical order 
  allowed_repos = [
    "akhileshmishrabiz/Devops-zero-to-hero",
    #"orgname/reponame"
  ]

   allowed_branches = [
    "main",
    "release-rc",
  ]

  # Create the condition string for all combinations
  sub_conditions = join(" || ", flatten([
    # For each repo
    for repo in local.allowed_repos : [
      # Add condition for each branch
      [for branch in local.allowed_branches :
      "(assertion.sub=='repo:${repo}:ref:refs/heads/${branch}')"],
      # Add pull request condition
      ["(assertion.sub=='repo:${repo}:pull_request')"]
    ]
  ]))

}

resource "google_project_service" "wif_api" {
  for_each = toset([
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}

resource "google_project_iam_member" "github-access" {

  project = "your_project_id"
  role    = "roles/owner"
  member  = "serviceAccount:${google_service_account.github-svc.email}"
}

# These resources are imported from gcp to harden the security and strictly allow particular 
# Repos under SOME_ORG org
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



