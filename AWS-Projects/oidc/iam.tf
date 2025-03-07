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
