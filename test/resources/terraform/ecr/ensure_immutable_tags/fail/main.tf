resource "aws_ecr_repository" "fail" {
  name                 = "my-mutable-ecr-repo"
  image_tag_mutability = "MUTABLE"
}
