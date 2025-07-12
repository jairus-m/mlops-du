"""
Module to define re-used constants like asset paths, names, etc.
Typicallly, I'd define these in a separate env or config file but
implementing here to keep assignment submission/monorepo simple.
"""

from pathlib import Path

# Use pathlib.Path for better path handling
BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "assets" / "data" / "IMDB Dataset.csv"
MODEL_PATH = BASE_DIR / "assets" / "models" / "sentiment_model.pkl"
KAGGLE_DATASET_PATH = "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"
KAGGLE_DATASET_NAME = "IMDB Dataset.csv"
LOG_PATH = BASE_DIR / "assets" / "logs" / "app.log"
