# OIDC Provider
resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
  
  client_id_list = [
    "sts.amazonaws.com"
  ]
  
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]

  tags = {
    Name = "GitHub-Actions-OIDC-Provider"
  }
}

# IAM Role
resource "aws_iam_role" "github_actions_eks_deploy_role" {
  name = "GitHubActionsEKSDeployRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" = [
              for repo in var.github_repositories : 
                "repo:${repo.org}/${repo.repo}:${repo.branch}"
            ]
          }
        }
      }
    ]
  })

  tags = {
    Name = "GitHub-Actions-EKS-Deploy-Role"
  }
}
