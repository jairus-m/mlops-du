"""
Pydantic models for the FastAPI app
"""

from pydantic import BaseModel


class PredictRequest(BaseModel):
    """Request Pydanticmodel for sentiment prediction sent to the API
    as a JSON object with a single key "text".

    Example request:
        {
            "text": "This movie was fantastic! I really enjoyed it."
        }
    """

    text: str


class SentimentResponse(BaseModel):
    """Response model for sentiment prediction returned by the API
    as a key-value pair with a single key "sentiment".

    Example response:
        {
            "sentiment": "positive"
        }
    """

    sentiment: str


class SentimentProbabilityResponse(BaseModel):
    """Response model for sentiment prediction with probability score returned by the API
    as a key-value pair with a two keys: "sentiment" and "probability".

    Example response:
        {
            "sentiment": "positive",
            "probability": 0.92
        }
    """

    sentiment: str
    probability: float


class ExampleResponse(BaseModel):
    """Response model for example movie review returned by the API
    as a key-value pair with a single key "review".

    Example response:
        {
            "review": "One of the best films I've seen this year..."
        }
    """

    review: str
