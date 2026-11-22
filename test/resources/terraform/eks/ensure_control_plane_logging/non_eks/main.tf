resource "aws_s3_bucket" "ignored_bucket" {
  bucket = "non-eks-scope-isolation-bucket"
}
