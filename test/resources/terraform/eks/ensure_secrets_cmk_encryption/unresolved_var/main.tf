variable "kms_key_arn" {
  type        = string
  description = "KMS key ARN without default, triggering Checkov directory runner limitation"
}

resource "aws_eks_cluster" "unresolved_var_cluster" {
  name     = "unresolved-var-cluster"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  encryption_config {
    resources = ["secrets"]
    provider {
      key_arn = var.kms_key_arn
    }
  }

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
