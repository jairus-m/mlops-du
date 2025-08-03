import logging
import json
from logging.handlers import RotatingFileHandler
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class JsonFormatter(logging.Formatter):
    """
    Formats log records as JSON strings.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt)
        }
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        else:
            log_record["message"] = record.getMessage()
        
        return json.dumps(log_record)

def setup_prediction_logger(config: dict) -> logging.Logger:
    """
    Sets up a logger for predictions based on the provided configuration.
    Args:
        config (dict): The application configuration.
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger("prediction_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent logs from being passed to the root logger

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    log_config = config.get("prediction_logging", {})
    handler_type = log_config.get("handler")

    if handler_type == "file":
        log_path_str = log_config.get("path", "assets/logs/prediction_logs.json")
        log_path = PROJECT_ROOT / log_path_str
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        fh = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5)
        fh.setFormatter(JsonFormatter())
        logger.addHandler(fh)
        
    elif handler_type == "dynamodb":
        # PLACEHOLDER FOR DYNAMODB HANDLER
        logger.warning(
            "DynamoDB logging is configured but not yet implemented. "
            "Prediction logs will not be sent to DynamoDB."
        )
       
        logger.addHandler(logging.NullHandler())
        
    else:
        logger.error(f"Invalid prediction_logging handler: {handler_type}")
        logger.addHandler(logging.NullHandler())

    return logger