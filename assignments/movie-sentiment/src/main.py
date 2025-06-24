import subprocess
from src.utils import(
    setup_logging,
    download_kaggle_dataset,
    DATA_PATH,
    MODEL_PATH
)

logger = setup_logging()

def main():
    """Main entry point for the movie sentiment analysis application."""
    if not MODEL_PATH.exists() and DATA_PATH.exists():
        logger.info("Training model since model file doesn't exist and IMDB data is present...")
        subprocess.run(["python", "-m", "src.train.train_model"])
    elif MODEL_PATH.exists():
        logger.info("Model file already exists, skipping training...")
    else:
        subprocess.run(["python", "-m", "src.train.train_model"])

    # Run Streamlit app
    logger.info("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "src/streamlit/app.py"])

if __name__ == "__main__":
    main()
