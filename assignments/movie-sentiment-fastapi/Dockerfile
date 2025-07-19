FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set wd
WORKDIR /movie-sentiment-fastapi

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Pre-train the model during build time
RUN uv run python -c "from src.ml.train_model import run_training; run_training()"

# Configure and expose port
# Using PORT as an ARG to allow for overriding the port at build time
# Default port reused from Streamlit assignment
ARG PORT=8501
ENV PORT=${PORT}
EXPOSE ${PORT}

# Using exec to handle signals properly and enable variable expansion
CMD ["sh", "-c", "exec uv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]