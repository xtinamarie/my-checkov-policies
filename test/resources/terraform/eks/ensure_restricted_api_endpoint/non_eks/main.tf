resource "aws_s3_bucket" "ignored_bucket" {
  bucket = "non-eks-endpoint-isolation-bucket"
}
