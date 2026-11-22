# Fails: missing encryption_config block (defaults to unencrypted or AWS-owned key)
resource "aws_eks_cluster" "fail_missing_config" {
  name     = "fail-missing-encryption-config"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}

# Fails: encryption_config present but provider.key_arn is empty string
resource "aws_eks_cluster" "fail_empty_key" {
  name     = "fail-empty-key-arn"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  encryption_config {
    resources = ["secrets"]
    provider {
      key_arn = ""
    }
  }

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
