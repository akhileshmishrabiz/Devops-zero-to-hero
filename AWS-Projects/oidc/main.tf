provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "github_repositories" {
  description = "List of GitHub repositories to grant access to"
  type = list(object({
    org    = string
    repo   = string
    branch = optional(string, "*")
  }))
  default = [
    {
      org    = "akhileshmishrabiz"
      repo   = "DevOpsDojo"
      branch = "*"
    }
  ]
}

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

# IAM Policy
resource "aws_iam_policy" "github_actions_eks_policy" {
  name        = "GitHubActionsEKSPolicy"
  description = "Policy for GitHub Actions to access EKS and ECR"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "eks:DescribeCluster",
          "eks:ListClusters"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Name = "GitHub-Actions-EKS-Policy"
  }
}

# Policy Attachment
resource "aws_iam_role_policy_attachment" "github_actions_eks_policy_attachment" {
  role       = aws_iam_role.github_actions_eks_deploy_role.name
  policy_arn = aws_iam_policy.github_actions_eks_policy.arn
}

# Outputs
output "role_arn" {
  description = "ARN of the IAM role for GitHub Actions"
  value       = aws_iam_role.github_actions_eks_deploy_role.arn
}

output "oidc_provider_arn" {
  description = "ARN of the OIDC provider"
  value       = aws_iam_openid_connect_provider.github_actions.arn
}
