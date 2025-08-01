# This resource defines a random string to be appended to the S3 bucket name.
# This helps ensure the bucket name is globally unique.
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Reference an existing S3 bucket instead of creating one
# The bucket must be created manually first
data "aws_s3_bucket" "movie_sentiment_assets" {
  bucket = var.s3_bucket
}

# This output block will display the S3 bucket name
output "s3_bucket_name" {
  description = "The name of the S3 bucket for storing assets."
  value       = data.aws_s3_bucket.movie_sentiment_assets.bucket
}