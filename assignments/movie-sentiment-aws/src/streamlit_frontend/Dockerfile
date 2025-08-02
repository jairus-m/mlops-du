# Dockerfile for the Streamlit Frontend

FROM python:3.12-slim

# Set environment variables for non-interactive installation
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install uv

COPY ./src/streamlit_frontend ./src/streamlit_frontend
COPY ./src/utils ./src/utils
COPY ./config.yaml ./config.yaml
COPY ./assets ./assets
COPY pyproject.toml ./

# Install dependencies using uv that are specific to the frontend
RUN uv pip install --system --no-cache ".[frontend]"

# Expose the port the app runs on
EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit_frontend/app.py"]
