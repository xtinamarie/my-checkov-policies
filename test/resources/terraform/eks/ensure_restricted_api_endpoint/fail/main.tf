# Fails: default configuration where endpoint_public_access defaults to true and CIDR defaults to 0.0.0.0/0
resource "aws_eks_cluster" "fail_default_public" {
  name     = "fail-default-public-endpoint"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids = [
      "subnet-12345678",
      "subnet-87654321"
    ]
  }
}

# Fails: explicit public access enabled with 0.0.0.0/0 allowed
resource "aws_eks_cluster" "fail_explicit_0_0_0_0" {
  name     = "fail-explicit-public-anywhere"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = true
    public_access_cidrs    = ["0.0.0.0/0"]
  }
}

# Fails: public access allowed to private subnet plus 0.0.0.0/0
resource "aws_eks_cluster" "fail_includes_0_0_0_0" {
  name     = "fail-includes-public-anywhere"
  role_arn = "arn:aws:iam::123456789012:role/eks-role"

  vpc_config {
    subnet_ids             = ["subnet-12345678", "subnet-87654321"]
    endpoint_public_access = true
    public_access_cidrs    = [
      "10.0.0.0/16",
      "0.0.0.0/0"
    ]
  }
}
