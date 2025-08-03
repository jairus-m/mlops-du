"""
Utility functions for the movie sentiment analysis project.

This module handles environment-aware configuration, logging, and asset management
(fetching from local disk in development or S3 in production).
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any
import boto3
import yaml
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from .prediction_logger import setup_prediction_logger


# Load environment variables from .env file
load_dotenv()

# Define project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_config() -> Dict[str, Any]:
    """
    Loads configuration from config.yaml based on the APP_ENV environment variable.

    Merges default settings with environment-specific settings.
    Exits the application if the configuration cannot be loaded.

    Returns:
        Dict[str, Any]: The fully loaded configuration dictionary.
    """
    env = os.getenv("APP_ENV", "development")
    config_path = PROJECT_ROOT / "config.yaml"

    try:
        with open(config_path, "r") as f:
            full_config = yaml.safe_load(f)

        # Start with default config
        config = full_config.get("default", {})
        # Merge in environment-specific config
        env_config = full_config.get(env, {})

        # Deep merge for nested dictionaries like 'paths'
        for key, value in env_config.items():
            if isinstance(value, dict) and isinstance(config.get(key), dict):
                config[key].update(value)
            else:
                config[key] = value

        config["env"] = env
        config["project_root"] = PROJECT_ROOT
        return config
    except FileNotFoundError:
        logging.critical(f"Config file not found at {config_path}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Error loading configuration: {e}")
        sys.exit(1)


def setup_logger(config: Dict[str, Any]) -> logging.Logger:
    """
    Sets up a rotating file logger and a console logger based on config.

    Args:
        config (Dict[str, Any]): The application configuration.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    log_config = config.get("main_logging", {})
    handler_type = log_config.get("handler")

    if handler_type == "file":
        log_path_str = log_config.get("path", "assets/logs/app.log")
        log_path = PROJECT_ROOT / log_path_str
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # File handler
        fh = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


config = load_config()
logger = setup_logger(config)
prediction_logger = setup_prediction_logger(config)
logger.info(f"Configuration loaded for '{config['env']}' environment.")


def upload_to_s3(local_path: Path, s3_key: str) -> bool:
    """
    Uploads a local file to an S3 bucket.

    Args:
        local_path (Path): The path to the local file to upload.
        s3_key (str): The destination key (path) in the S3 bucket.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        logger.critical("S3_BUCKET_NAME is not configured. Cannot upload.")
        return False

    try:
        s3 = boto3.client("s3")
        logger.info(f"Uploading {local_path.name} to s3://{bucket}/{s3_key}...")
        s3.upload_file(str(local_path), bucket, s3_key)
        logger.info("Upload to S3 successful!")
        return True
    except ClientError as e:
        logger.error(f"Failed to upload to S3: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during S3 upload: {e}")
        return False


def download_from_s3(bucket: str, key: str, local_path: Path) -> bool:
    """
    Downloads a file from an S3 bucket to a local path.

    Args:
        bucket (str): The S3 bucket name.
        key (str): The key (path) of the object in the bucket.
        local_path (Path): The local destination path.

    Returns:
        bool: True if download was successful or file already exists, False otherwise.
    """
    if local_path.exists():
        logger.info(f"File {local_path} already exists locally. Skipping S3 download.")
        return True
    try:
        s3 = boto3.client("s3")
        logger.info(f"Downloading s3://{bucket}/{key} to {local_path}...")
        local_path.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(bucket, key, str(local_path))
        logger.info("Download complete.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.error(f"S3 object not found: s3://{bucket}/{key}")
        else:
            logger.error(f"Error downloading from S3: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during S3 download: {e}")
        return False


def get_asset_path(asset_key: str) -> Path:
    """
    Returns the local filesystem path for a given asset key (e.g., 'model', 'data').

    In 'production' mode, it downloads the asset from S3 to a temporary local
    directory (assets) and returns the path to the local copy.
    In 'development' mode, it returns the direct local path from the config.

    Args:
        asset_key (str): The key for the asset, as defined in config.yaml.

    Returns:
        Path: The local, ready-to-use path for the asset.
    """
    path_info = config["paths"][asset_key]

    if config["env"] == "production":
        bucket = os.getenv("S3_BUCKET_NAME")
        s3_key = path_info
        if not bucket or not s3_key:
            logger.critical("S3 bucket name or key is not configured in environment.")
            sys.exit(1)

        local_path = PROJECT_ROOT / "assets" / Path(s3_key).name
        if not download_from_s3(bucket, s3_key, local_path):
            logger.critical(f"Failed to retrieve required asset {s3_key} from S3.")
            sys.exit(1)
        return local_path
    else:
        dev_path = PROJECT_ROOT / path_info
        if not dev_path.exists():
            logger.critical(f"Asset '{asset_key}' not found at local path: {dev_path}")
            sys.exit(1)
        return dev_path


__all__ = [
    "config",
    "logger",
    "get_asset_path",
    "upload_to_s3",
    "prediction_logger",
]
