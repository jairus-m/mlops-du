"""
Module for loading the sentiment analysis model, validating its existence,
and triggering training if it does not exist.
"""

from typing import Callable
from pathlib import Path
from sklearn.pipeline import Pipeline
import joblib
from src.utils import logger, get_asset_path
from src.sklearn_training.train_model import run_training


def load_model(model_path: Path) -> Pipeline:
    """
    Load model pickle file from a given path.
    Args:
        model_path (Path): Path to the model file.
    Returns:
        Pipeline: The loaded model.
    """
    try:
        return joblib.load(model_path)
    except Exception as e:
        logger.error(f"Error loading model from {model_path}: {e}")
        raise


def initialize_model(training_function: Callable[[], None] = run_training) -> Pipeline:
    """
    Initializes the model.

    This function first checks if the model exists locally or in S3 (per environment).
    - If it exists, it loads it.
    - If it does not exist, it triggers the training function, then loads the new model.

    The actual path resolution (local vs. S3) is handled by get_asset_path.

    Args:
        training_function (Callable): The function to call to train a new model.

    Returns:
        Pipeline: The loaded or newly trained model.
    """
    try:
        # get_asset_path will download from S3 if in prod and the file exists.
        # If the file doesn't exist in S3, it will fail, triggering the exception.
        model_path = get_asset_path("model")
        logger.info("Model found, loading from path...")
        model = load_model(model_path)
    except SystemExit:
        # This is triggered by get_asset_path if the model doesn't exist in prod
        logger.warning("Model not found in production environment. Triggering training...")
        training_function()
        # After training, the model should exist in S3, so we try getting it again.
        model_path = get_asset_path("model")
        model = load_model(model_path)

    # The original code had a local-only check.
    # This new version relies on the S3 check within get_asset_path for production.
    # For local dev, if the model is missing, we also train.
    if not model_path.exists():
        logger.warning(f"Model not found at {model_path}. Triggering training...")
        training_function()
        model = load_model(model_path)

    logger.info("Model initialized successfully.")
    return model
