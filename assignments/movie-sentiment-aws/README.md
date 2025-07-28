# Movie Sentiment Analysis - AWS Deployment

This project deploys a movie sentiment analysis application on AWS using a fully automated Terraform setup. The architecture consists of a FastAPI backend and a Streamlit frontend, each running in a Docker container on a separate EC2 instance.

## 🏗️ Architecture

- **Backend**: FastAPI service running on a dedicated EC2 instance.
- **Frontend**: Streamlit application running on a dedicated EC2 instance.
- **Infrastructure**: All AWS resources (EC2, S3, Security Groups) are managed by Terraform.
- **Automation**: EC2 instances are provisioned with startup scripts (`user_data`) that automatically clone the project repository, build the Docker images, and run the containers.

## 📋 Prerequisites

- **AWS Account**: An AWS account with programmatic access.
- **Terraform**: [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed on your local machine.
- **Git**: [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your local machine.
- **Repository Access**: A Git repository URL for your project. If the repository is private, the URL must include an access token.

## Configuration

This project uses a different configuration method depending on the environment.

### Local Development (`.env` file)

For running the application on your local machine, configuration is managed via a `.env` file in the project root. This file is used to set variables like `APP_ENV="development"`, your AWS credentials, and the backend URL.

### AWS Deployment (`terraform.tfvars`)

When deploying to AWS with Terraform, configuration is passed directly to the EC2 instances at launch time. **This method does not use the `.env` file.**

Key variables are handled as follows:

-   **`APP_ENV`**: This is automatically set to `"production"` inside the startup scripts in `terraform/ec2.tf`.
-   **AWS Credentials**: These are passed securely from your `terraform.tfvars` file to the Docker containers.
-   **`API_BACKEND_URL`**: This is dynamically set by Terraform to the private IP address of the backend instance, ensuring the frontend can communicate with it.

---

## 🚀 Automated Deployment Workflow

This workflow provisions the entire infrastructure and deploys the application with a single command.

### Step 1: Configure Your Environment

1.  **Clone this Repository**

    If you haven't already, clone the project to your local machine.

2.  **Set AWS Credentials as Environment Variables**

    Terraform will use these variables to authenticate with your AWS account.

    ```bash
    export AWS_ACCESS_KEY_ID="your_access_key_here"
    export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
    export AWS_SESSION_TOKEN="your_session_token_here"
    ```

3.  **Manually Create S3 Bucket**
    
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

4.  **Create a Terraform Variables File**

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

    # The HTTPS URL of the Git repository to clone
    # For a private GitHub repo, use a Personal Access Token (PAT):
    # repository_url = "https://<your_github_username>:<your_pat>@github.com/user/repo.git"
    repository_url = "https://github.com/your-username/your-repo.git"

    # The AWS region to deploy to
    aws_region = "us-east-1"
    ```

### Step 2: Deploy the Application

1.  **Initialize Terraform**

    From the `terraform` directory, run `terraform init` to prepare the workspace.

    ```bash
    terraform init
    ```

2.  **Apply the Terraform Plan**

    Run `terraform apply` to create the AWS resources and deploy the application. Terraform will show you a plan and ask for confirmation before proceeding.

    ```bash
    terraform apply
    ```

    This process will take a few minutes as the EC2 instances need to start, install dependencies, clone the repository, and build the Docker images.

### Step 3: Access Your Application

Once the `terraform apply` command is complete, it will output the public IP address of the frontend application.

- **Frontend URL**: `http://<FRONTEND_PUBLIC_IP>:8501`

You can find this URL in the `frontend_public_ip` output from Terraform.

---

## 🧹 Cleanup

To tear down all the AWS resources created by this project, run the `destroy` command from the `terraform` directory.

```bash
terraform destroy
```

## 🔧 Troubleshooting

- **Deployment Failures**: Check the EC2 instance logs in the AWS Console (EC2 -> Instances -> Select Instance -> Actions -> Monitor and troubleshoot -> Get system log). This will show the output of the `user_data` script.
- **Application Not Responding**:
    - Verify the security groups allow traffic on ports 8000 and 8501.
    - SSH into the instance using the command from `terraform output ssh_command` and check the Docker container status with `docker ps`.
    - Check the container logs with `docker logs <container_name>`.
- **Git Clone Fails**: Ensure the `repository_url` is correct and includes an access token if the repository is private.

## 🔒 Security

- The `terraform.tfvars` file contains sensitive credentials and should **never** be committed to version control.
- The provided security groups are permissive for demonstration purposes. For a production environment, you should restrict the `cidr_blocks` to known IP addresses.