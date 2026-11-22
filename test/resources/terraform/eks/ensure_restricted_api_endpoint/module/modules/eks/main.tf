resource "aws_eks_cluster" "module_cluster" {
  name     = "module-eks-restricted-endpoint"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = false
  }
}
