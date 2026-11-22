resource "aws_eks_cluster" "module_cluster" {
  name     = "module-eks-cluster"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
