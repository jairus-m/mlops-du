import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
from src.utils import setup_logging, DATA_PATH, MODEL_PATH

logger = setup_logging()


def load_and_preprocess_data(data_path: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess the IMDB dataset.
    Returns features (X) and labels (y).
    Args:
        data_path (str): Path to the IMDB dataset
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
    X = df['review'].values
    y = df['sentiment'].replace({'negative': 0, 'positive': 1}).values
    
    logger.info(f"Features (X) shape: {X.shape}")
    logger.info(f"Labels (y) shape: {y.shape}")
    logger.info(f"Label distribution: {np.bincount(y)}")
    
    return X, y

def create_and_train_model(X, y) -> Pipeline:
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
    
    # Create the pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()), # Add params?
        ('classifier', MultinomialNB()) # Add params?
    ])
    logger.info(f"Pipeline created successfully: {pipeline.named_steps}")
    
    logger.info("Training the model...")
    pipeline.fit(X, y)
    
    logger.info("Model training completed!")
    
    train_score = pipeline.score(X, y)
    logger.info(f"Training accuracy: {train_score:.4f}")
    
    return pipeline

def save_model(pipeline, model_path) -> None:
    """
    Save the trained model pipeline as a pickle file
    to a specified path.
    Args:
        pipeline (Pipeline): Trained pipeline
        model_path (str): Path to save the model
    Returns:
        None
    """
    logger.info(f"Saving model to {model_path}...")
    
    joblib.dump(pipeline, model_path)
    
    # Verify the model was saved correctly
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        logger.info(f"Model saved successfully! File size: {file_size:.2f} MB")
    else:
        logger.error("Error: Model file was not created!")

def main():
    """
    Main entry point for the training process.
    """
    logger.info("IMDB Sentiment Analysis Model Training")
    
    try:
        X_train, y_train = load_and_preprocess_data(DATA_PATH)
        
        pipeline = create_and_train_model(X_train, y_train)
        
        save_model(pipeline, MODEL_PATH)
        
        logger.info("Training completed successfully!")
        logger.info(f"Model saved to {MODEL_PATH}")
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    main()
