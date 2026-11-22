resource "aws_eks_cluster" "pass_exact" {
  name     = "compliant-eks-exact-logging"
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

resource "aws_eks_cluster" "pass_all" {
  name     = "compliant-eks-all-logging"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}
