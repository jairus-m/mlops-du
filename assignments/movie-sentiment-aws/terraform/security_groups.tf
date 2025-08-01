# This security group is for the Streamlit frontend instance.
resource "aws_security_group" "frontend" {
  name        = "streamlit-frontend-sg"
  description = "Allow HTTP traffic to Streamlit frontend"

  # Allow incoming traffic on port 8501 (Streamlit) from anywhere.
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # "0.0.0.0/0" means from any IP address
  }

  # Allow SSH access from anywhere (for deployment)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outgoing traffic. This is needed to connect to the backend,
  # pull Docker images, and install packages.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # "-1" means all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "Streamlit Frontend SG"
    Project   = "Movie-Sentiment-AWS"
    ManagedBy = "Terraform"
  }
}

# This security group is for the FastAPI backend instance.
resource "aws_security_group" "backend" {
  name        = "fastapi-backend-sg"
  description = "Allow traffic from frontend to FastAPI backend"

  # Allow incoming traffic on port 8000 (FastAPI) from anywhere.
  # This allows the frontend to connect to the backend via public IP.
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow from anywhere for public IP access
  }

  # Allow SSH access from anywhere (for deployment)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outgoing traffic.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "FastAPI Backend SG"
    Project   = "Movie-Sentiment-AWS"
    ManagedBy = "Terraform"
  }
}
