# COMP 4450 MLOps
This repo contains all the sub-repos representing each assignment. 

## Dependency Management
The entire monorepo dependency graph is managed by [uv](https://docs.astral.sh/uv/) and uses the [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) feature. This allows __all packages__ within the monorepo to share a single lockfile and a consistent set of dependencies and at the same time, enabling each package to define its own `pyproject.toml`. This greatly simplifies dependency resolution, installation, and script execution for all sub-repos/packages/workspace members. Within each workspace package, I try to add straightforward instructions to execute the individual assignments scripts/apps.

## Contents 
All assignments are under `assignments/`:

#### Assignment 1: Movie Sentiment ML Pipeline & Streamlit App
- `movie-sentiment/`



