"""
Module for loading the sentiment analysis model from the models directory
and validating its existence. Trains the model if it does not exist.
"""

from typing import Optional, Callable
from sklearn.pipeline import Pipeline
import joblib
from src.utils import logger
from src.sklearn_training.train_model import run_training


def load_model(model_path: str) -> Pipeline:
    """
    Load model pickle file.
    Args:
        model_path (str): Path to the model file
    Returns:
        model (Pipeline): The loaded model
    Raises:
        FileNotFoundError: If model file doesn't exist
        Exception: If model loading fails
    """
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}")
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")


def model_exists(model_path: str) -> bool:
    """
    Check if model file exists.
    Args:
        model_path (str): Path to the model file
    Returns:
        bool: True if model exists, False otherwise
    """
    try:
        joblib.load(model_path)
        return True
    except (FileNotFoundError, Exception):
        return False


def validate_model(model_path: str) -> Optional[Pipeline]:
    """
    Validate the model file exists and is a valid model.
    Args:
        model_path (str): Path to the model file
    Returns:
        Optional[Pipeline]: The loaded model if valid, None otherwise
    """
    if not model_exists(model_path):
        logger.info("Model file does not exist.")
        return None

    try:
        model = load_model(model_path)
        logger.info("Model file exists. Model Loaded.")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return None


def initialize_model(
    model_path: str, training_function: Callable[[], None] = run_training
) -> Pipeline:
    """
    Initialize model by loading existing model or training new one.
    Args:
        model_path (str): Path to the model file
        training_function (Callable): Function to call for training
    Returns:
        Pipeline: The loaded or newly trained model
    """
    model = validate_model(model_path)

    if model is None:
        logger.info("Training model...")
        training_function()
        model = load_model(model_path)

    return model
