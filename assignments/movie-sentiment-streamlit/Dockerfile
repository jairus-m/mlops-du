FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set wd
WORKDIR /movie-sentiment-streamlit

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Install project as editable package
RUN uv pip install -e .

# Expose Streamlit port (refer to https://docs.streamlit.io/deploy/tutorials/docker)
# Using PORT as an ARG to allow for overriding the port at build time
ARG PORT=8501
ENV PORT=${PORT}
EXPOSE ${PORT}

# Default command
# Using exec to handle signals properly and enable variable expansion
  CMD ["sh", "-c", "exec uv run streamlit run src/streamlit/app.py --server.port ${PORT}"]