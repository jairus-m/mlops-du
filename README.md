# COMP 4450 MLOps
This repo contains all the subrepos (aka "projects") that represent each assignment. 

## Prerequisites
- `uv>=0.7.10`
  - [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- `task>=3.43.3`
  - [task installation](https://taskfile.dev/installation/)
- Docker Desktop (Contains both the Engine and CLI Client)
  - [docker installation](https://docs.docker.com/desktop/)

__Note__: For easy setup on macOS/Linux, use the included installation script after cloning the repo:
```bash
git clone https://github.com/jairus-m/mlops-du.git
cd mlops-du 
bash install-tools.sh
```
This shell script will install `uv` and `task` if they're not already present and will verify the installation.

## Dependency Management
The entire monorepo dependency graph is managed by [uv](https://docs.astral.sh/uv/) and uses the [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) feature. This allows __all packages__ within the monorepo to share a single lockfile and a consistent set of dependencies and at the same time, enabling each package to define its own `pyproject.toml`. This greatly simplifies dependency resolution, installation, and script execution for all sub-repos/packages/workspace members. Within each workspace package, I try to add straightforward instructions to execute the individual assignments scripts/apps.

## Task Execution
Assignments are ran with [task](https://taskfile.dev/) which is a task runner/build tool that provides a simple and consistent way to execute each assignment's main entry point script or various other CLI commands.
- __Note:__ All subrepos are under `assignments/` and are also reffered to as "projects". For example, `mlops-du/assignments/movie-sentiment-streamlit` is both a subrepo and project.

---

## Assignments

### Assignment 1: Movie Sentiment ML Pipeline & Streamlit App
- `movie-sentiment-streamlit/`
  - Run command: `task execute-proj PROJ=movie-sentiment-streamlit`

### Assignment 2: Use Docker to Run Movie Sentiment ML Pipeline & Streamlit App
- `movie-sentiment-streamlit/`
  - Run commands:
    - Build Docker Container: `task build PROJ=movie-sentiment-streamlit`
    - Run Docker Container: `task run PROJ=movie-sentiment-streamlit`
    - Remove Docker Image: `task clean PROJ=movie-sentiment-streamlit`
    - Build + Run Docker Container: `task execute-proj-docker PROJ=movie-sentiment-streamlit`

### Assignment 3: Use FastAPI to Serve Movie Sentiment ML Model
- `movie-sentiment-fastapi/`
  - Run commands:
    - Build Docker Container: `task build PROJ=movie-sentiment-fastapi`
    - Run Docker Container: `task run PROJ=movie-sentiment-fastapi`
    - Remove Docker Image: `task clean PROJ=movie-sentiment-fastapi`
    - Build + Run Docker Container: `task execute-proj-docker PROJ=movie-sentiment-fastapi`
    
### Assignment 5: Local E2E Deployment of Movie Sentiment ML Application (dev)
- `movie-sentiment-aws/`
  - Run all services: `task aws-dev:up`
  - Get logs: `task aws-dev:logs`
  - Stop all services: `task aws-dev:down`

### [WIP] Assignment 6: AWS Deployment of Movie Sentiment ML Application (prod)
- `movie-sentiment-aws/`
  - This project is currently a work in progress...
  - Not currently ran with `task` as local configuration, multiple terminal sessions, and complexities exist with deploying to AWS
  - Navigate to the deployment repo and follow the detailed step-by-step `README.md` instructions
    - `cd assignments/movie-sentiment-aws`

---

## Exporting Dependencies to `requirements.txt`
To export a `requirements.txt` file that lists out all the dependencies within `assignments/<project-name>`, run the following from the root:
```bash
uv export --directory assignments/<project-name> -o requirements.txt
```

## Overriding Default Port
The default PORT of `8501` (used accross all assignments) can be overidden with the `PORT` var:
```bash
# Build Docker image to expose PORT 8123 and pass to the CMD argument
task build PROJ=<projet-name> PORT=8123
# Run Docker image to map to PORT 8123
task run PROJ=<projet-name> PORT=8123
```
