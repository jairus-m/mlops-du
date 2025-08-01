# Movie Sentiment Analysis - AWS Deployment

This project deploys a movie sentiment analysis application on AWS using a fully automated Terraform setup. The architecture consists of a FastAPI backend, a Streamlit frontend, and  ML training. Each service runs in a Docker container on their own dedicated EC2 instances.

This project is structured as a multi-package monorepo using `uv` workspaces. Each application (`fastapi_backend`, `streamlit_frontend`, `sklearn_training`) has its own modules and dependencies while sharing a single `uv.lock` file at the root.

## Basic Architecture

This project is a MINIMAL deployment approach to serving an ML model. This is purely for learning purposes and is missing a lot of MLOps best-practices in terms of observability, monitoring, re-training, CI/CD, etc.

<img src="assets/images/architecture.png" width="1000"/>


### Filetree
```bash
.
├── assets
│   ├── data # Local data stored/staged here
│   ├── logs # App logs 
│   └── models # Local model stored/staged here
├── config.yaml # Sets env-aware variables/paths
├── pyproject.toml # Dependencies
├── README.md
├── src
│   ├── fastapi_backend # Backend service
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── model_loader.py
│   │   └── schemas.py
│   ├── sklearn_training # ML training service
│   │   ├── Dockerfile
│   │   ├── data_loader.py
│   │   └── train_model.py
│   └── streamlit_frontend # Frontend service
│   │   ├── Dockerfile
│   │   └── app.py
│   └── utils # Shared utils (S3 interaction) need to refactor this..
└── terraform
   ├── ec2.tf # EC2 config
   ├── modules # Re-usable modules for Docker deployment
   │   └── docker_deployment
   │       ├── main.tf
   │       └── variables.tf
   ├── providers.tf
   ├── s3.tf # S3 config
   ├── security_groups.tf # Security group config
   └── variables.tf # Expected vars
```


- ML Training:
  - Traning service on EC2 to download data, train ML model, and push data/model file to S3
- Backend: 
  - FastAPI inference service running on EC2
- Frontend: 
  - Streamlit application running on EC2
- Storage:
  - Data and model file are uploaded, stored, and retrieved from S3
- Infrastructure and Automation: 
  - All AWS resources (EC2, S3, Security Groups) are managed by Terraform.
    - At a high level, EC2 instances are provisioned by Terraform which uses remote-exec provisioners to SSH into each instance after launch. These scripts install Docker/Git/other dependencies, transfer files, build the required Docker images, and orchestrates the three service's containers with the correct environment variables. Configuration files are copied as needed and services are started automatically!

## Local Dev Deployment 

### Prerequisites
- `uv>=0.7.10`
  - [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- `task>=3.43.3`
  - [task installation](https://taskfile.dev/installation/)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your local machine.

### Local Configuration
For running this project on your local machine, no configuration is needed. The application will use your local files instead of S3 for storage and your CPU for computation.

### Local Development with Docker Compose
For a streamlined and consistent development experience that mirrors the production environment locally, you can use Docker Compose and the custom `task` commands.
From the root of the project (`mlops-du/`), you can use the following commands:
1.  Build and Start All Services

    This single command builds the Docker images for ML training, the FastAPI backend, and the Stramlit frontend, and then starts them in the correct order. It will first run the training container to generate the model and then launch the backend and frontend services.

    ```bash
    task aws-dev:up
    ```

    You will see the logs from all services streamed to your terminal.

2.  Access the Application

    -   **Frontend URL**: [http://localhost:8501](http://localhost:8501)
    -   **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

3.  View Logs (in a separate terminal)

    If you want to follow the logs of the running services without blocking your main terminal, you can run:

    ```bash
    task aws-dev:logs
    ```

4.  Stop and Clean Up

    To stop all the running services and remove the containers and network, run:

    ```bash
    task aws-dev:down
    ```

## AWS Prod Deployment 

### Prerequisites
- The following need to be installed:
  - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - Need an AWS account with programmatic access along with the following credentials:
      - aws_access_key_id
      - aws_secret_access_key
      - aws_session_token
  - [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed on your local machine.
  - [uv](https://github.com/astral-sh/uv) installed on your local machine.
  - Docker Desktop (Contains both the Engine and CLI Client)
    - [docker installation](https://docs.docker.com/desktop/)

### Configuration for AWS Deployment
Within `mlops-du/assignments/movie-sentiment-aws`, create an `.env` file and add the following:
```
# For AWS CLI / Boto3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=

# For Terraform (re-using the same values as above)
TF_VAR_aws_access_key_id=$AWS_ACCESS_KEY_ID
TF_VAR_aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
TF_VAR_aws_session_token=$AWS_SESSION_TOKEN
```
While these AWS credentials are really only used in production, they are needed locally for Terraform for authentication in order to run CLI commands like `plan` and `apply` as well as for passing directly to the EC2 instances at launch time.


## AWS Deployment with Terraform

This workflow provisions the entire infrastructure and deploys the applications with Terraform.

### Step 1: Initialize Terraform and Create S3 Bucket

1.  Initialize Terraform

    From the root of the project (`mlops-du/`), run the following command to initialize Terraform. This will download the necessary providers and set up the backend.

    ```bash
    task aws-prod:init
    ```

2.  Create the S3 Bucket

    Next, create the S3 bucket that will be used to store the model and data artifacts.

    ```bash
    task aws-prod:s3 S3_BUCKET=<your-unique-bucket-name> # Defaults to movie-sentiment-s3
    ```

    > **Note**: Because the `awsstudent` role has very limited permissions, there are issues with Terraform when it tries to automatically check the state of some resources (S3 mainly) via the object lock. Because of this, you have to manually create an S3 bucket.

### Step 2: Deploy the Application

1.  Apply the Terraform Plan

    Run the following command to create the AWS resources and deploy the application. Terraform will show you a plan and ask for confirmation before proceeding.

    ```bash
    task aws-prod:apply S3_BUCKET=<your-unique-bucket-name> # Defaults to movie-sentiment-s3
    ```

    This process will take a few minutes as the EC2 instances need to start, transfer necessary application files, install dependencies, build the Docker images, and run them.

### Step 3: Access the App

Once the `terraform apply` command is complete, it will output the public IP address of the frontend application.

- **Frontend URL**: `http://<FRONTEND_PUBLIC_IP>:8501`

### Step 4: Cleanup

To tear down all the AWS resources created by this project, run the `destroy` command from the `terraform` directory.

  ```bash
  task aws-prod:destroy
  ```


# Screenshots

#### Terraform CLI Output 
<img src="assets/images/terraform.png" width="800"/>

#### S3 Bucket
<img src="assets/images/s3.png" width="800"/>

#### EC2 Instances
<img src="assets/images/ec2.png" width="800"/>

#### FastAPI Backend Docs Endpoint
<img src="assets/images/fastapi.png" width="800"/>

#### Streamlit Frontend
<img src="assets/images/streamlit.png" width="800"/>
