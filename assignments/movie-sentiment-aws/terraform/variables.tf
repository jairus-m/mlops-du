variable "aws_access_key_id" {
  description = "AWS access key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS secret access key"
  type        = string
  sensitive   = true
}

variable "aws_session_token" {
  description = "AWS session token (if required)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "project_path" {
  description = "The relative path from the repository root to the project directory."
  type        = string
  default     = "assignments/movie-sentiment-aws"
}
