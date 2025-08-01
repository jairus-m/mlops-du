"""
Module for loading the sentiment analysis model.
"""

import sys
import joblib
from sklearn.pipeline import Pipeline
from src.utils import logger, get_asset_path


def load_model() -> Pipeline:
    """
    Loads the sentiment analysis model.

    This function fetches the model from the path determined by the environment
    (local or S3) and loads it into memory. If the model cannot be loaded,
    it logs a critical error and exits the application.

    Returns:
        Pipeline: The loaded scikit-learn model pipeline.
    """
    try:
        logger.info("Attempting to load sentiment analysis model...")
        model_path = get_asset_path("model")
        model = joblib.load(model_path)
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.critical(f"Failed to load model. Error: {e}")
        sys.exit(1)
