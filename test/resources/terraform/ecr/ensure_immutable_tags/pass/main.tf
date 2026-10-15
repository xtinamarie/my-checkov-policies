resource "aws_ecr_repository" "pass" {
  name                 = "my-immutable-ecr-repo"
  image_tag_mutability = "IMMUTABLE"
}
