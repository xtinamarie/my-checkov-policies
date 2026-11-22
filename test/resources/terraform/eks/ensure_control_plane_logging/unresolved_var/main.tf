variable "cluster_log_types" {
  type        = list(string)
  description = "Cluster log types without default, triggering Checkov directory runner limitation"
}

resource "aws_eks_cluster" "unresolved_var_cluster" {
  name     = "unresolved-var-cluster"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  enabled_cluster_log_types = var.cluster_log_types

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
