import os
import shutil
import logging
from pathlib import Path
import kagglehub

# Use pathlib.Path for better path handling
BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "assets" / "data" / "IMDB Dataset.csv"
MODEL_PATH = BASE_DIR / "assets" / "models" / "sentiment_model.pkl"
KAGGLE_DATASET_PATH = "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"
KAGGLE_DATASET_NAME = "IMDB Dataset.csv"


def setup_logging() -> logging.Logger:
    """
    Configure logging with appropriate format and level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def download_kaggle_dataset(
    kaggle_dataset_path: str = KAGGLE_DATASET_PATH,
    kaggle_dataset_name: str = KAGGLE_DATASET_NAME,
) -> None:
    """
    Downloads the IMDB dataset from Kaggle and saves it to DATA_PATH.
    Args:
        kaggle_dataset_path (str): The path to the Kaggle dataset
        kaggle_dataset_name (str): The expectedname of the CSV file to download
    Returns:
        None
    """
    logger = setup_logging()

    # Ensure the data directory exists
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    path = kagglehub.dataset_download(kaggle_dataset_path)

    # Handle path - kagglehub returns a list or string
    downloaded_path = Path(path[0] if isinstance(path, list) else path)

    logger.info(
        f"Downloading dataset from https://www.kaggle.com/datasets/{kaggle_dataset_path}..."
    )

    # Look for the CSV file directly in the downloaded directory
    csv_file = downloaded_path / kaggle_dataset_name
    if csv_file.exists():
        shutil.copy(csv_file, DATA_PATH)
    else:
        # Fallback: search for any CSV file
        csv_files = list(downloaded_path.glob("*.csv"))
        if csv_files:
            shutil.copy(csv_files[0], DATA_PATH)
        else:
            raise FileNotFoundError("No CSV file found in downloaded dataset")

    logger.info(f"Dataset downloaded and saved to {DATA_PATH}")
