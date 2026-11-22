resource "aws_eks_cluster" "module_cluster" {
  name     = "module-eks-cmk-secrets"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  encryption_config {
    resources = ["secrets"]
    provider {
      key_arn = "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
    }
  }

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
