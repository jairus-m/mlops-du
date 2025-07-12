"""
Module for downloading the IMDB dataset from Kaggle if not already present in the specified path.
"""

from pathlib import Path
import shutil
from src.utils import KAGGLE_DATASET_PATH, KAGGLE_DATASET_NAME, DATA_PATH
from src.utils import logger
import kagglehub


def download_kaggle_dataset(
    kaggle_dataset_path: str = KAGGLE_DATASET_PATH,
    kaggle_dataset_name: str = KAGGLE_DATASET_NAME,
) -> None:
    """
    Downloads a dataset from Kaggle and saves it to DATA_PATH.
    Args:
        kaggle_dataset_path (str): The path to the Kaggle dataset
        kaggle_dataset_name (str): The expectedname of the CSV file to download
    Returns:
        None
    """
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
