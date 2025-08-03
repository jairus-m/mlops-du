"""
FastAPI Movie Sentiment Analysis API

This API provides endpoints for sentiment analysis of movie reviews.
It is environment-aware and can load assets from local disk or S3.
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
import pandas as pd
from src.utils import (
    logger,
    get_asset_path,
    prediction_logger,
)
from src.fastapi_backend.utils.middleware import (
    log_middleware_request,
    log_middleware_response,
)
from src.fastapi_backend.utils.schemas import (
    PredictRequest,
    SentimentFeedback,
    SentimentResponse,
    SentimentProbabilityResponse,
    ExampleResponse,
)
from src.fastapi_backend.utils.model_loader import load_model

app = FastAPI()

# Middleware to log requests and responses
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware_request)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware_response)

# Load the model on startup
model = load_model()
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
        sentiment = "positive" if prediction == 1 else "negative"
        
        
        prediction = {
            "endpoint": "/predict",
            "request_text": request.text,
            "predicted_sentiment": sentiment,
        }
        prediction_logger.info(prediction)
        
        return {"sentiment": sentiment}
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
            
        prediction = {
            "endpoint": "/predict_proba",
            "request_text": request.text,
            "predicted_sentiment": prediction_str,
            "probability": round(probability, 2),
        }
        prediction_logger.info(prediction)
    
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
        # Get the path to the dataset, which may be downloaded from S3
        data_path = get_asset_path("data")
        df = pd.read_csv(data_path)
        random_review = df.sample(n=1)["review"].iloc[0]
        return {"review": random_review}
    except Exception as e:
        logger.error(f"Error getting random review: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving example review")
    

@app.post("/true_sentiment")
async def true_sentiment(request: SentimentFeedback) -> dict:
    """
    True sentiment endpoint
    Args:
        request (TrueSentimentRequest):  {"is_sentiment_correct": "bool"}
    """
    try:
        feedback = {
            "endpoint": "/true_sentiment",
            "request_text": request.request_text,
            "predicted_sentiment": request.predicted_sentiment,
            "probability": request.probability,
            "true_sentiment": request.true_sentiment,
        }
        prediction_logger.info(feedback)
        logger.info({"true_sentiment": feedback["true_sentiment"]})
        return {"message": "Feedback received"}
    except Exception as e:
        logger.error(f"Error processing sentiment feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing sentiment feedback")

@app.get("/favicon.ico")
async def favicon():
    """
    Handles constant favicon requests from browser
    to prevent 404 Error logs.
    """
    return Response(status_code=204, content="No favicon here!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
