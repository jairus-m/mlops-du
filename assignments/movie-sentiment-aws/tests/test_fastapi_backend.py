from unittest.mock import patch
import pandas as pd


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict(client, mock_prediction_logger):
    """Test prediction endpoint"""
    response = client.post("/predict", json={"text": "Great movie!"})
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}
    mock_prediction_logger.info.assert_called_once()


def test_predict_proba(client, mock_prediction_logger):
    """Test probability prediction endpoint"""
    response = client.post("/predict_proba", json={"text": "Great movie!"})
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive", "probability": 0.9}
    mock_prediction_logger.info.assert_called_once()


def test_example(client):
    """Test example endpoint"""
    mock_df = pd.DataFrame({"review": ["A random review."]})
    with (
        patch("src.fastapi_backend.main.pd.read_csv", return_value=mock_df),
        patch(
            "src.fastapi_backend.main.get_asset_path",
            return_value="/mock/path/data.csv",
        ),
    ):
        response = client.get("/example")
        assert response.status_code == 200
        assert response.json() == {"review": "A random review."}


def test_true_sentiment(client, mock_prediction_logger):
    """Test feedback endpoint"""
    feedback_data = {
        "request_text": "An okay movie",
        "predicted_sentiment": "positive",
        "probability": 0.8,
        "true_sentiment": "negative",
        "is_sentiment_correct": False,
    }
    response = client.post("/true_sentiment", json=feedback_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback received"}
    mock_prediction_logger.info.assert_called_once()
