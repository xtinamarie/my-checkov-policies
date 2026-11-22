# Fails: missing enabled_cluster_log_types attribute (defaults to disabled in AWS)
resource "aws_eks_cluster" "fail_missing_all" {
  name     = "fail-missing-all-logging"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}

# Fails: partial log types, missing required "authenticator" stream
resource "aws_eks_cluster" "fail_partial" {
  name     = "fail-partial-logging"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  enabled_cluster_log_types = [
    "api",
    "audit"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}

# Fails: empty enabled_cluster_log_types list
resource "aws_eks_cluster" "fail_empty" {
  name     = "fail-empty-logging"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  enabled_cluster_log_types = []

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
