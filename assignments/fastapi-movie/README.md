# FastAPI Movie Sentiment Analysis API

A REST API that performs sentiment analysis on movie reviews using a machine learning model. The API provides endpoints for predicting sentiment (positive/negative) and retrieving example reviews from the IMDB dataset.


## Project Structure
```bash
fastapi-movie/
├── assets/
│   ├── data/                       # Dataset directory
│   ├── docs/                       # Documentation
│   ├── images/                     # Image assets
│   ├── logs/                       # App logs
│   └── models/                     # Model file
├── src/
│   ├── schemas/                    # Pydantic Models
│   ├── train/                      # ML Training
│   ├── utils/                      # Utils
│   └── main.py                     # Main entry point to run FastAPI App
├── Dockerfile                      # Docker container config
├── pyproject.toml                  # Python dependencies
└── README.md                       # Submission docs 
```

## Installation and Setup 
For prerequisites, installation instructions, and setup details, please see the top-level `README.md` file. It contains information about required dependencies, how to clone the repository, and instructions for running the installation script. It also goes over how to run and execute assignments with `task`.

### Run Options

#### Without Docker
```bash
task execute-proj PROJ=fastapi-movie
```

#### With Docker
To run each Docker command step-by-step:
```bash
# Build Docker Container
task build PROJ=fastapi-movie

# Run Docker Container
task run PROJ=fastapi-movie

# Clean up: Remove Docker Image
task clean PROJ=fastapi-movie
```

To run Docker build and run in one command:
```bash
# Build and run Docker Container
task execute-proj-docker PROJ=fastapi-movie

# Clean up: Remove Docker Image
task clean PROJ=fastapi-movie
```

## API Endpoints

- `GET /`: Root endpoint that returns a welcome message
- `GET /health`: Health check endpoint
- `POST /predict`: Predicts sentiment (positive/negative) for a given review text
- `POST /predict_proba`: Predicts sentiment with probability score
- `GET /example`: Returns a random movie review from the dataset

#### Docs Site
- http://0.0.0.0:8501/docs

<img src="assets/images/docs.png" width="1000"/>

#### Predict
- http://0.0.0.0:8501/predict

<img src="assets/images/post__predict.png" width="1000"/>

#### Predict with Probabilities
- http://0.0.0.0:8501/predict_proba

<img src="assets/images/post__predict_proba.png" width="1000"/>

#### Example Reviews
- http://0.0.0.0:8501/example

<img src="assets/images/get__example.png" width="1000"/>
