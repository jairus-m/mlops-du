# This resource creates a new key pair. Terraform will generate a new key
# and you must save the private key to a file to be able to SSH into the instances.
resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = tls_private_key.rsa.public_key_openssh
}

# This is a helper resource to generate the RSA private key.
resource "tls_private_key" "rsa" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# This local sensitive file resource saves the generated private key to your local machine.
# IMPORTANT: This file should be added to your .gitignore and treated like a password.
resource "local_sensitive_file" "private_key" {
  content  = tls_private_key.rsa.private_key_pem
  filename = "${path.module}/deployer-key.pem"
}

# SKLearn Model Training EC2 instance
resource "aws_instance" "ml_training" {
  instance_type = "t2.micro"
  ami           = data.aws_ami.amazon_linux.id

  vpc_security_group_ids = [aws_security_group.backend.id]
  key_name               = aws_key_pair.deployer.key_name

  tags = {
    Name      = "SKLearn Model Training Instance"
    Project   = "Movie-Sentiment-AWS"
    ManagedBy = "Terraform"
  }
}

# Backend EC2 instance
resource "aws_instance" "backend" {
  depends_on = [
    aws_instance.ml_training,
  ]
  instance_type = "t2.micro"
  ami           = data.aws_ami.amazon_linux.id

  vpc_security_group_ids = [aws_security_group.backend.id]
  key_name               = aws_key_pair.deployer.key_name

  tags = {
    Name      = "FastAPI Backend Instance"
    Project   = "Movie-Sentiment-AWS"
    ManagedBy = "Terraform"
  }
}

# Frontend EC2 instance
resource "aws_instance" "frontend" {
  depends_on = [
    aws_instance.backend
  ]
  instance_type = "t2.micro"
  ami           = data.aws_ami.amazon_linux.id

  vpc_security_group_ids = [aws_security_group.frontend.id]
  key_name               = aws_key_pair.deployer.key_name

  tags = {
    Name      = "Streamlit Frontend Instance"
    Project   = "Movie-Sentiment-AWS"
    ManagedBy = "Terraform"
  }
}

# For the SKLearn Model Training instance
resource "null_resource" "run_ml_training" {
  triggers = {
    always_run = "${timestamp()}"
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = tls_private_key.rsa.private_key_pem
    host        = aws_instance.ml_training.public_ip
  }

  # Wait for SSH to be ready
  provisioner "remote-exec" {
    inline = ["echo 'SSH is ready'"]
  }

  # Create the destination directory structure
  provisioner "remote-exec" {
    inline = ["mkdir -p /home/ec2-user/app/src"]
  }

  provisioner "file" {
    source      = "${path.module}/../src/sklearn_training"
    destination = "/home/ec2-user/app/src/sklearn_training"
  }

  provisioner "file" {
    source      = "${path.module}/../src/utils"
    destination = "/home/ec2-user/app/src/utils"
  }

  provisioner "file" {
    source      = "${path.module}/../assets"
    destination = "/home/ec2-user/app/assets"
  }

  provisioner "file" {
    source      = "${path.module}/../config.yaml"
    destination = "/home/ec2-user/app/config.yaml"
  }

  provisioner "file" {
    source      = "${path.module}/../pyproject.toml"
    destination = "/home/ec2-user/app/pyproject.toml"
  }

  # Build and run the training Docker container
  provisioner "remote-exec" {
    inline = [
      "sudo yum install -y docker",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo usermod -a -G docker ec2-user",
      "sudo chmod 666 /var/run/docker.sock",
      "cd /home/ec2-user/app",
      "ls -la",
      "docker --version",
      "docker build -f src/sklearn_training/Dockerfile -t movie-sentiment-training .",
      "docker run -d --name training -e APP_ENV=production -e AWS_ACCESS_KEY_ID=${var.aws_access_key_id} -e AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key} -e AWS_SESSION_TOKEN=${var.aws_session_token} -e S3_BUCKET_NAME=${data.aws_s3_bucket.movie_sentiment_assets.bucket} movie-sentiment-training:latest"
    ]
  }
}

# For the backend instance
resource "null_resource" "upload_backend_files" {
  depends_on = [
    null_resource.run_ml_training,
  ]
  triggers = {
    always_run = "${timestamp()}"
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = tls_private_key.rsa.private_key_pem
    host        = aws_instance.backend.public_ip
  }

  # Wait for SSH to be ready
  provisioner "remote-exec" {
    inline = ["echo 'SSH is ready'"]
  }

  # Create the destination directory
  provisioner "remote-exec" {
    inline = ["mkdir -p /home/ec2-user/app/src"]
  }

  provisioner "file" {
    source      = "${path.module}/../src/fastapi_backend"
    destination = "/home/ec2-user/app/src/fastapi_backend"
  }

  provisioner "file" {
    source      = "${path.module}/../src/utils"
    destination = "/home/ec2-user/app/src/utils"
  }

  provisioner "file" {
    source      = "${path.module}/../assets"
    destination = "/home/ec2-user/app/assets"
  }

  provisioner "file" {
    source      = "${path.module}/../config.yaml"
    destination = "/home/ec2-user/app/config.yaml"
  }

  provisioner "file" {
    source      = "${path.module}/../pyproject.toml"
    destination = "/home/ec2-user/app/pyproject.toml"
  }

  # Build and run the backend Docker container
  provisioner "remote-exec" {
    inline = [
      "sudo yum install -y docker",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo usermod -a -G docker ec2-user",
      "sudo chmod 666 /var/run/docker.sock",
      "cd /home/ec2-user/app",
      "ls -la",
      "docker --version",
      "docker build -f src/fastapi_backend/Dockerfile -t movie-sentiment-backend .",
      "docker run -d --name backend -p 8000:8000 --restart=always -e APP_ENV=production -e AWS_ACCESS_KEY_ID=${var.aws_access_key_id} -e AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key} -e AWS_SESSION_TOKEN=${var.aws_session_token} -e S3_BUCKET_NAME=${data.aws_s3_bucket.movie_sentiment_assets.bucket} movie-sentiment-backend:latest"
    ]
  }
}

# For the frontend instance
resource "null_resource" "upload_frontend_files" {
  depends_on = [
    null_resource.upload_backend_files,
  ]
  triggers = {
    always_run = "${timestamp()}"
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = tls_private_key.rsa.private_key_pem
    host        = aws_instance.frontend.public_ip
  }

  # Wait for SSH to be ready
  provisioner "remote-exec" {
    inline = ["echo 'SSH is ready'"]
  }

  # Create the destination directory
  provisioner "remote-exec" {
    inline = ["mkdir -p /home/ec2-user/app/src"]
  }

  provisioner "file" {
    source      = "${path.module}/../src/streamlit_frontend"
    destination = "/home/ec2-user/app/src/streamlit_frontend"
  }

  provisioner "file" {
    source      = "${path.module}/../src/utils"
    destination = "/home/ec2-user/app/src/utils"
  }

  provisioner "file" {
    source      = "${path.module}/../assets"
    destination = "/home/ec2-user/app/assets"
  }

  provisioner "file" {
    source      = "${path.module}/../config.yaml"
    destination = "/home/ec2-user/app/config.yaml"
  }

  provisioner "file" {
    source      = "${path.module}/../pyproject.toml"
    destination = "/home/ec2-user/app/pyproject.toml"
  }

  # Build and run the frontend Docker container
  provisioner "remote-exec" {
    inline = [
      "sudo yum install -y docker",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo usermod -a -G docker ec2-user",
      "sudo chmod 666 /var/run/docker.sock",
      "cd /home/ec2-user/app",
      "ls -la",
      "docker --version",
      "docker build -f src/streamlit_frontend/Dockerfile -t movie-sentiment-frontend .",
      "docker run -d --name frontend -p 8501:8501 --restart=always -e APP_ENV=production -e API_BACKEND_URL=http://${aws_instance.backend.public_ip}:8000 -e AWS_ACCESS_KEY_ID=${var.aws_access_key_id} -e AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key} -e AWS_SESSION_TOKEN=${var.aws_session_token} -e S3_BUCKET_NAME=${data.aws_s3_bucket.movie_sentiment_assets.bucket} movie-sentiment-frontend:latest"
    ]
  }
}


# Data source to find the latest Amazon Linux AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Outputs

output "frontend_url" {
  description = "HTTP URL for accessing the Streamlit frontend."
  value       = "http://${aws_instance.frontend.public_ip}:8501"
}

output "frontend_public_ip" {
  description = "Public IP address of the Streamlit frontend instance."
  value       = aws_instance.frontend.public_ip
}

output "backend_public_ip" {
  description = "Public IP address of the FastAPI backend instance."
  value       = aws_instance.backend.public_ip
}

output "ssh_command_frontend" {
  description = "Command to SSH into the frontend instance."
  value       = "ssh -i ${local_sensitive_file.private_key.filename} ec2-user@${aws_instance.frontend.public_ip}"
}

output "ssh_command_backend" {
  description = "Command to SSH into the frontend instance."
  value       = "ssh -i ${local_sensitive_file.private_key.filename} ec2-user@${aws_instance.backend.public_ip}"
}

