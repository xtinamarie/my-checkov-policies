# Passes: public endpoint access is disabled (private only)
resource "aws_eks_cluster" "pass_private_only" {
  name     = "pass-private-only-endpoint"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = false
  }
}

# Passes: public access is enabled but restricted to specific corporate CIDRs (no 0.0.0.0/0)
resource "aws_eks_cluster" "pass_restricted_cidrs" {
  name     = "pass-restricted-cidrs-endpoint"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = true
    public_access_cidrs    = [
      "10.0.0.0/16",
      "192.168.1.0/24"
    ]
  }
}
