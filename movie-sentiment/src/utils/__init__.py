import os
import logging

# Use os.path.join and make paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, 'assets', 'data', 'IMDB Dataset.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'assets', 'models', 'sentiment_model.pkl')

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