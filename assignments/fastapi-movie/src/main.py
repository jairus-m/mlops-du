"""
FastAPI Movie Sentiment Analysis API

This API provides endpoints for sentiment analysis of movie reviews.
"""

import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils import (
    logger,
    log_middleware_request,
    log_middleware_response,
    download_kaggle_dataset,
    MODEL_PATH,
    DATA_PATH,
)
from src.schemas import (
    PredictRequest,
    SentimentResponse,
    SentimentProbabilityResponse,
    ExampleResponse,
)
from src.ml import initialize_model

app = FastAPI()

# Middleware to log requests and responses
# Refer to https://github.com/fastapi/fastapi/issues/678 for more info on implementation
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware_request)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware_response)

# Initialize model and handles training if model does not exist
model = initialize_model(MODEL_PATH)
logger.info("FastAPI App initialized successfully!")


@app.get("/")
async def root() -> dict:
    """
    Root endpoint
    Returns:
        dict: A dictionary with a message indicating the API is running
    """
    return {"message": "FastAPI Movie Sentiment Analysis API"}


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint
    Returns:
        dict: A dictionary with the health status of the API
    """
    try:
        # Check if model has required methods
        assert hasattr(model, "predict")
        assert hasattr(model, "predict_proba")
        assert callable(model.predict)
        assert callable(model.predict_proba)

        return {
            "status": "healthy",
            "model_loaded": MODEL_PATH.exists(),
            "dataset_available": DATA_PATH.exists(),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/predict")
async def predict(request: PredictRequest) -> SentimentResponse:
    """
    Predict sentiment endpoint
    Args:
        request (PredictRequest):  {"text": "string"}
    Returns:
        SentimentResponse object
    """
    try:
        prediction = model.predict([request.text])[0]
        return {"sentiment": "positive" if prediction == 1 else "negative"}
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error making prediction")


@app.post("/predict_proba")
async def predict_proba(request: PredictRequest) -> SentimentProbabilityResponse:
    """
    Predict sentiment with probability endpoint based on the input text.
    Args:
        request (PredictRequest):  {"text": "string"}
    Returns:
        SentimentProbabilityResponse object
    """
    try:
        prediction_int = model.predict([request.text])[0]
        probabilities = model.predict_proba([request.text])[0]
        if prediction_int == 1:
            prediction_str = "positive"
            probability = probabilities[1]
        else:
            prediction_str = "negative"
            probability = probabilities[0]
        return {"sentiment": prediction_str, "probability": round(probability, 2)}
    except ValueError as e:
        logger.error(f"Pydantic validation error: {str(e)}")
        raise HTTPException(status_code=422, detail="Invalid input format")
    except Exception as e:
        logger.error(f"Error making prediction with probabilities: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error making prediction with probabilities"
        )


@app.get("/example")
async def example() -> ExampleResponse:
    """
    Example endpoint to get a random review from the dataset
    Returns:
        ExampleResponse object
    """
    try:
        df = pd.read_csv(DATA_PATH)
        random_review = df.sample(n=1)["review"].iloc[0]
        return {"review": random_review}
    except FileNotFoundError:
        logger.info("Dataset file does not exist. Downloading dataset...")
        download_kaggle_dataset()
        df = pd.read_csv(DATA_PATH)
        random_review = df.sample(n=1)["review"].iloc[0]
        return {"review": random_review}
    except Exception as e:
        logger.error(f"Error getting random review: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving example review")


@app.get("/favicon.ico")
async def favicon():
    """
    Handles constant favicon requests from browser
    to prevent 404 Error logs.
    """
    return Response(status_code=204, content="No favicon here!")
