
import pandas as pd
import json
import os
from src.utils import get_asset_path, config, logger

def load_imdb_dataset() -> pd.DataFrame:
    """
    Loads the IMDB dataset.
    Uses get_asset_path to be environment-aware (local vs. S3).
    Returns:
        pd.DataFrame: The loaded IMDB dataset.
    """
    try:
        logger.info("Attempting to load IMDB dataset...")
        data_path = get_asset_path("data")
        df = pd.read_csv(data_path)
        logger.info("IMDB dataset loaded successfully.")
        return df
    except Exception as e:
        logger.error(f"Failed to load IMDB dataset. Error: {e}")
        return pd.DataFrame()

def load_all_logs() -> list:
    """
    Loads all logs from the prediction log file.
    Returns:
        list: A list of all logs.
    """
    logs = []
    env = config.get("env")

    if env == "development":
        log_config = config.get("prediction_logging", {})
        log_path_str = log_config.get("path")
        if not log_path_str:
            logger.warning("Prediction log path not configured.")
            return logs
            
        log_file = os.path.join(config["project_root"], log_path_str)
        
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    logs = [json.loads(line) for line in f]
                logger.info(f"Loaded {len(logs)} logs from {log_file}.")
            except Exception as e:
                logger.error(f"Error reading or parsing log file {log_file}: {e}")
        else:
            logger.warning(f"Log file not found at {log_file}.")
            
    elif env == "production":
        logger.warning("DynamoDB log loading not yet implemented.")
        # PLACEHOLDER FOR DYNAMODB LOG LOADING
        
    return logs

def load_feedback_logs() -> list:
    """
    Filters all logs to return only those with feedback.
    Returns:
        list: A list of feedback logs.
    """
    all_logs = load_all_logs()
    feedback_logs = [log for log in all_logs if log.get("endpoint") == "/true_sentiment" and "true_sentiment" in log]
    logger.info(f"Found {len(feedback_logs)} feedback logs.")
    return feedback_logs
