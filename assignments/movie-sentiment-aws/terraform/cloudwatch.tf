# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "movie_sentiment" {
  name              = "/aws/ec2/movie-sentiment-app"
  retention_in_days = 14

  tags = {
    Environment = "production"
    Project     = "Movie-Sentiment-AWS"
    ManagedBy   = "Terraform"
  }
}


