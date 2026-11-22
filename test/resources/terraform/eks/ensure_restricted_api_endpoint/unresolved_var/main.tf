variable "endpoint_public_access" {
  type        = bool
  description = "Public endpoint flag without default, triggering Checkov directory runner limitation"
}

resource "aws_eks_cluster" "unresolved_var_cluster" {
  name     = "unresolved-var-cluster"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = var.endpoint_public_access
  }
}
