import subprocess
from src.utils import DATA_PATH, MODEL_PATH, setup_logging

logger = setup_logging()

def main():
    """Main entry point for the movie sentiment analysis application."""
    if not MODEL_PATH.exists() and DATA_PATH.exists():
        logger.info("Training model since model file doesn't exist and IMDB data is present...")
        subprocess.run(["python", "-m", "src.train.train_model"])
    elif MODEL_PATH.exists():
        logger.info("Model file already exists, skipping training...")
    else:
        logger.info(
            "Warning: IMDB dataset not found. Please download it from: "
            "https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews "
            "and place it in the `assets/data/` directory."
        )
        return

    # Run Streamlit app
    logger.info("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "src/streamlit/app.py"])

if __name__ == "__main__":
    main()
