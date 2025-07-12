"""
Module for training the sentiment analysis model based on the IMDB dataset.
The model is saved as a pickle file to the models directory.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from src.utils import (
    logger,
    download_kaggle_dataset,
    DATA_PATH,
    MODEL_PATH,
    KAGGLE_DATASET_PATH,
    KAGGLE_DATASET_NAME,
)

pd.set_option("future.no_silent_downcasting", True)


def load_and_preprocess_data(data_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess the IMDB dataset.
    Returns features (X) and labels (y).
    Args:
        data_path (Path): Path to the IMDB dataset
    Returns:
        X (np.ndarray): Training data / features (X)
        y (np.ndarray): Training Labels / target (y)
    """
    logger.info("Loading IMDB dataset...")
    logger.info(f"Data path: {data_path}")

    df = pd.read_csv(data_path)

    logger.info(f"Dataset loaded successfully! Shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Sentiment distribution:\n{df['sentiment'].value_counts()}")

    # Split into features (X) and labels (y)
    X = df["review"].values
    y = df["sentiment"].replace({"negative": 0, "positive": 1}).astype(int).values

    logger.info(f"Features (X) shape: {X.shape}")
    logger.info(f"Labels (y) shape: {y.shape}")
    logger.info(f"Label distribution: {np.bincount(y)}")

    return X, y


def create_and_train_model_pipeline(X, y) -> Pipeline:
    """
    Create and train the sentiment analysis pipeline.
    Returns the trained pipeline.
    Args:
        X (np.ndarray): Features (X)
        y (np.ndarray): Labels (y)
    Returns:
        pipeline (Pipeline): Trained pipeline
    """
    logger.info("Creating and training the model pipeline...")

    # Create the pipeline w/ optional params
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=10000,  # Limit vocabulary size
                    min_df=2,  # Minimum document frequency
                    max_df=0.95,  # Maximum document frequency ?
                    ngram_range=(1, 2),  # Use unigrams and bigrams ?
                    stop_words="english",  # Remove English stop words
                ),
            ),
            (
                "classifier",
                MultinomialNB(
                    alpha=1.0,  # Smoothing parameter (default = 1)
                    fit_prior=True,  # Learn class prior probabilities (default = True)
                    class_prior=None,  # Uniform prior distribution (default = None)
                ),
            ),
        ]
    )
    logger.info(f"Pipeline created successfully: {pipeline.named_steps}")

    logger.info("Training the model...")
    pipeline.fit(X, y)

    logger.info("Model training completed!")

    train_score = pipeline.score(X, y)
    logger.info(f"Training accuracy: {train_score:.4f}")

    return pipeline


def save_model(pipeline, model_path: Path) -> None:
    """
    Save the trained model pipeline as a pickle file
    to a specified path.
    Args:
        pipeline (Pipeline): Trained pipeline
        model_path (Path): Path to save the model
    Returns:
        None
    """
    logger.info(f"Saving model to {model_path}...")

    joblib.dump(pipeline, model_path)

    # Verify the model was saved correctly
    if model_path.exists():
        file_size = model_path.stat().st_size / (1024 * 1024)  # MB
        logger.info(f"Model saved successfully! File size: {file_size:.2f} MB")
    else:
        logger.error("Error: Model file was not created!")


def run_training():
    """
    Main entry point for the training process.
    """
    logger.info("IMDB Sentiment Analysis Model Training")

    try:
        if DATA_PATH.exists():
            logger.info("IMDB dataset found, loading and preprocessing data...")
        else:
            download_kaggle_dataset(
                kaggle_dataset_path=KAGGLE_DATASET_PATH,
                kaggle_dataset_name=KAGGLE_DATASET_NAME,
            )
            logger.info("IMDB dataset downloaded, loading and preprocessing data...")

        X_train, y_train = load_and_preprocess_data(DATA_PATH)

        pipeline = create_and_train_model_pipeline(X_train, y_train)

        save_model(pipeline, MODEL_PATH)

        logger.info("Training completed successfully!")
        logger.info(f"Model saved to {MODEL_PATH}")

    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise
