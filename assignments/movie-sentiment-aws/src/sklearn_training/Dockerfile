# Dockerfile for the FastAPI Backend

# Use a slim, official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for non-interactive installation
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install 'uv' for faster dependency management
RUN pip install uv

# Copy the dependency definition file
COPY pyproject.toml ./

# Install dependencies using uv
# This installs all dependencies listed in pyproject.toml
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy the application source code, config, and assets into the container
COPY ./src/sklearn_training ./src/sklearn_training
COPY ./src/utils ./src/utils
COPY ./config.yaml ./config.yaml
COPY ./assets ./assets

# Run training and keep container alive briefly to ensure S3 upload completes
CMD ["sh", "-c", "uv run python -c 'from src.sklearn_training.train_model import run_training; run_training()' && sleep 30"]
