FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set wd
WORKDIR /fastapi-movie

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Pre-train the model during build time
RUN uv run python -c "from src.ml.train_model import run_training; run_training()"

# Expose port (reusing Streamlit "default"port since Taskfile.yml is using it)
EXPOSE 8501

# Default command
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8501"]