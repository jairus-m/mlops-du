# COMP 4450 MLOps
This repo contains all the sub-repos representing each assignment. 

## Prerequisites
- `uv>=0.7.10`
  - [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
- `task>=3.43.3`
  - [task installation](https://taskfile.dev/installation/)

## Dependency Management
The entire monorepo dependency graph is managed by [uv](https://docs.astral.sh/uv/) and uses the [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) feature. This allows __all packages__ within the monorepo to share a single lockfile and a consistent set of dependencies and at the same time, enabling each package to define its own `pyproject.toml`. This greatly simplifies dependency resolution, installation, and script execution for all sub-repos/packages/workspace members. Within each workspace package, I try to add straightforward instructions to execute the individual assignments scripts/apps.

__NOTE__: To export a `requirements.txt` file that lists out all the dependencies within `assignments/<project-name>`, run the following from the root:
```bash
uv export --directory assignments/<project-name> -o requirements.txt
```

## Execution
Assignments are ran with [task](https://taskfile.dev/) which is a task runner/build tool that provides a simple and consistent way to execute each assignment's main entry point script.

To run an assignment for a project in its respective `assignments/<project-name>` directory, simply run the following in the CLI from the monorepo root directory `mlops-du/`:
```yaml
task <project-name>
```

## Contents 
All assignments are under `assignments/`

#### Assignment 1: Movie Sentiment ML Pipeline & Streamlit App
- `movie-sentiment/`
  - Run command: `task movie-sentiment`






