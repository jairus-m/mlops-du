import os
import logging
from pathlib import Path

# Use pathlib.Path for better path handling
BASE_DIR = Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / 'assets' / 'data' / 'IMDB Dataset.csv'
MODEL_PATH = BASE_DIR / 'assets' / 'models' / 'sentiment_model.pkl'

def setup_logging() -> logging.Logger:
    """
    Configure logging with appropriate format and level.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)