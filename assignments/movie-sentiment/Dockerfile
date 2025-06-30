FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set wd
WORKDIR /movie-sentiment

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Install project as editable package
RUN uv pip install -e .

# Expose Streamlit port (refer to https://docs.streamlit.io/deploy/tutorials/docker)
EXPOSE 8501

# Default command
CMD ["uv", "run", "python", "src/main.py"]