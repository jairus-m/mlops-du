"""
Module for training the sentiment analysis model and saving it.

In a 'development' environment, the model is saved locally.
In a 'production' environment, the model is uploaded to an S3 bucket.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

from src.core import (
    logger,
    config,
    PROJECT_ROOT,
    upload_to_s3,
)
from src.sklearn_training.utils.data_loader import download_kaggle_dataset

pd.set_option("future.no_silent_downcasting", True)


def load_and_preprocess_data(data_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess the IMDB dataset.
    Args:
        data_path (Path): Path to the IMDB dataset file.
    Returns:
        A tuple containing the features (X) and labels (y).
    """
    logger.info(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    logger.info(f"Dataset loaded successfully! Shape: {df.shape}")

    X = df["review"].values
    y = df["sentiment"].replace({"negative": 0, "positive": 1}).astype(int).values
    return X, y


def create_and_train_model_pipeline(X, y) -> Pipeline:
    """
    Create and train the sentiment analysis pipeline.
    Args:
        X (np.ndarray): Features (reviews).
        y (np.ndarray): Labels (sentiments).
    Returns:
        The trained scikit-learn pipeline.
    """
    logger.info("Creating and training the model pipeline...")
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=10000, stop_words="english")),
            ("classifier", MultinomialNB()),
        ]
    )
    pipeline.fit(X, y)
    logger.info("Model training completed!")
    logger.info(f"Training accuracy: {pipeline.score(X, y):.4f}")
    return pipeline


def save_model(pipeline: Pipeline) -> None:
    """
    Saves the trained model pipeline.

    - In 'development', saves to a local file path defined in config.
    - In 'production', saves to a temporary local file, uploads it to S3,
      and then deletes the temporary file.
    """
    env = config["env"]
    model_path_info = config["paths"]["model"]

    if env == "production":
        # Save to a temporary local file first for uploading
        temp_dir = PROJECT_ROOT / "assets"
        temp_dir.mkdir(exist_ok=True)
        local_path = temp_dir / Path(model_path_info).name
        logger.info(f"Saving model temporarily to {local_path} for S3 upload...")
        joblib.dump(pipeline, local_path)

        # Upload to S3 and then clean up
        s3_key = model_path_info
        if upload_to_s3(local_path, s3_key):
            logger.info(f"Removing temporary model file: {local_path}")
            os.remove(local_path)
    else:
        # In development, save directly to the local path
        local_path = PROJECT_ROOT / model_path_info
        local_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving model locally to {local_path}...")
        joblib.dump(pipeline, local_path)
        file_size = local_path.stat().st_size / (1024 * 1024)
        logger.info(f"Model saved successfully! File size: {file_size:.2f} MB")


def run_training():
    """
    Main entry point for the training process.
    """
    logger.info("Starting IMDB Sentiment Analysis Model Training...")
    try:
        # Download the dataset (which also handles S3 upload in prod)
        local_data_path = download_kaggle_dataset()

        # Load and preprocess the data from the local file
        X_train, y_train = load_and_preprocess_data(local_data_path)

        # Train the model
        pipeline = create_and_train_model_pipeline(X_train, y_train)

        # Save the model (which also handles S3 upload in prod)
        save_model(pipeline)

        logger.info("Training process completed successfully!")

    except Exception as e:
        logger.error(f"An unexpected error occurred during training: {e}")
        raise


if __name__ == "__main__":
    run_training()
