import subprocess
from src.utils import setup_logging, MODEL_PATH

logger = setup_logging()


def main():
    """Main entry point for the movie sentiment analysis application."""
    if MODEL_PATH.exists():
        logger.info("Model file already exists, skipping training...")
    else:
        logger.info("Model file not found.", "Training model...")
        # Note: train_model.py handles the download of the IMDB data if it doesn't exist
        subprocess.run(["python", "-m", "src.train.train_model"])

    # Run Streamlit app
    logger.info("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "src/streamlit/app.py"])


if __name__ == "__main__":
    main()
