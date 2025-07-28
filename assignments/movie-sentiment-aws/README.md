# Movie Sentiment Analysis - AWS Deployment

This project deploys a movie sentiment analysis application on AWS using a fully automated Terraform setup. The architecture consists of a FastAPI backend and a Streamlit frontend. Each runs in a Docker container on a separate EC2 instance.

## Architecture

- Backend: FastAPI service running on a dedicated EC2 instance.
- Frontend: Streamlit application running on a dedicated EC2 instance.
- Infrastructure: All AWS resources (EC2, S3, Security Groups) are managed by Terraform.
- Automation: EC2 instances are provisioned with startup scripts (`user_data`) that automatically clone the project repository, build the Docker images, and run the containers.

## Prerequisites

- AWS Account: An AWS account with programmatic access.
- Terraform: [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed on your local machine.

## Configuration

This project uses a different configuration method depending on the environment (development vs production).

### Local Development (`.env` file) via Local Files

For running this project on your local machine, configuration is managed via a `.env` file in the project root. The application will try to hit S3 for artifacts but will default to your local files if no credentials are found.

1. Navigate to `movie-sentiment-aws`

```bash
cd assignments/movie-sentiment-aws 
```

2. In the terminal, run FastAPI:

```bash  
uvicorn src.fastapi_backend.main:app --reload
```

3. In a nother teminal, run Streamlit:

```bash
cd assignments/movie-sentiment-aws   

uvicorn src.fastapi_backend.main:app --reload
```

### AWS Deployment (`terraform.tfvars`) via Terraform

When deploying to AWS with Terraform, configuration is passed directly to the EC2 instances at launch time. **This method does not use the `.env` file.**

Key variables are handled as follows:

-   APP_ENV: This is automatically set to `"production"` inside the startup scripts in `terraform/ec2.tf`.
-   AWS Credentials: These are passed securely from your `terraform.tfvars` file to the Docker containers.
-   API_BACKEND_URL: This is dynamically set by Terraform to the private IP address of the backend instance

---

## Automated Deployment Workflow

This workflow provisions the entire infrastructure and deploys the application with a single command.

### Step 1: Configure Your Environment

1. Clone this Repository

2. Set AWS Credentials as Environment Variables
    Terraform will use these variables to authenticate with your AWS account.
    ```bash
    export AWS_ACCESS_KEY_ID="your_access_key_here"
    export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
    export AWS_SESSION_TOKEN="your_session_token_here"
    ```

3. Manually Create S3 Bucket
    
    Because the `awsstudent` role has very limited permissions, there are issues with Terraform when it tries to automatically check the state of some resources (S3 mainly) via
    the object lock:
    ```bash
    AccessDenied: User: arn:aws:sts::614899697409:assumed-role/voclabs/user4228548=jairus is not authorized to perform: s3:GetBucketObjectLockConfiguration on resource: "arn:aws:s3:::movie-sentiment-s3-dig97dh6" with an explicit deny in an identity-based policy
    ```

    Because of this, you can manually create an S3 bucket either through the AWS Console or CLI. 
    ```bash
    # example
    aws s3api create-bucket --bucket movie-sentiment-s3 --region us-east-1
    ```

4. Create a Terraform Variables File

    Navigate to the `terraform` directory and create a file named `terraform.tfvars`. This file will securely store the variables needed for the deployment.

    ```bash
    cd assignments/movie-sentiment-aws/terraform
    ```

    Create the `terraform.tfvars` file with the following content:

    ```hcl
    # terraform/terraform.tfvars

    # Your AWS credentials (these will be passed to the EC2 instances)
    aws_access_key_id     = "your_access_key_here"
    aws_secret_access_key = "your_secret_key_here"
    aws_session_token   = "your_session_token_here"

    # The AWS region to deploy to
    aws_region = "us-east-1"

    # Project path within the repository (if different from root)
    project_path = "assignments/movie-sentiment-aws" 
    ```

### Step 2: Deploy the Application

1. Initialize Terraform
   From the `terraform` directory, run `terraform init` to prepare the workspace.

    ```bash
    terraform init
    ```

2.  Apply the Terraform Plan

    Run `terraform apply` to create the AWS resources and deploy the application. Terraform will show you a plan and ask for confirmation before proceeding.

    ```bash
    terraform apply
    ```

    This process will take a few minutes as the EC2 instances need to start, install dependencies, build the Docker images, and run them.

### Step 3: Access the App

Once the `terraform apply` command is complete, it will output the public IP address of the frontend application.

- **Frontend URL**: `http://<FRONTEND_PUBLIC_IP>:8501`


---

## 🧹 Cleanup

To tear down all the AWS resources created by this project, run the `destroy` command from the `terraform` directory.

```bash
terraform destroy
```

