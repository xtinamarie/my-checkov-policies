# Fails: Explicitly set to MUTABLE
resource "aws_ecr_repository" "fail_mutable" {
  name                 = "fail-mutable-repo"
  image_tag_mutability = "MUTABLE"
}

# Fails: Missing image_tag_mutability (Terraform defaults to MUTABLE)
resource "aws_ecr_repository" "fail_missing_mutability" {
  name = "fail-missing-mutability-repo"
}

# Fails: IMMUTABLE_WITH_EXCLUSION (verifies strict equality, not substring match)
resource "aws_ecr_repository" "fail_immutable_with_exclusion" {
  name                 = "fail-immutable-exclusion-repo"
  image_tag_mutability = "IMMUTABLE_WITH_EXCLUSION"
}

# Fails: MUTABLE_WITH_EXCLUSION
resource "aws_ecr_repository" "fail_mutable_with_exclusion" {
  name                 = "fail-mutable-exclusion-repo"
  image_tag_mutability = "MUTABLE_WITH_EXCLUSION"
}
