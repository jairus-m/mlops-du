"""
Configuration loader for the movie sentiment analysis project.
Loads settings from config.yaml and provides path resolution.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration class that loads settings from YAML file."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._resolve_paths()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _resolve_paths(self):
        """Resolve relative paths to absolute paths based on project root."""
        base_dir = Path(__file__).parent.parent.parent
        
        # Store resolved paths in a separate dict
        self._resolved_paths = {}
        for path_key, path_value in self._config['paths'].items():
            resolved_path = base_dir / path_value
            self._resolved_paths[path_key.upper()] = resolved_path
    
    @property
    def DATA_PATH(self) -> Path:
        return self._resolved_paths['DATA']
    
    @property
    def MODEL_PATH(self) -> Path:
        return self._resolved_paths['MODEL']
    
    @property
    def LOG_PATH(self) -> Path:
        return self._resolved_paths['LOGS']
    
    @property
    def KAGGLE_DATASET_PATH(self) -> str:
        return self._config['kaggle']['dataset_path']
    
    @property
    def KAGGLE_DATASET_NAME(self) -> str:
        return self._config['kaggle']['dataset_name']


# Global config instance
config = Config()

# Export the same interface as the old constants
DATA_PATH = config.DATA_PATH
MODEL_PATH = config.MODEL_PATH
LOG_PATH = config.LOG_PATH
KAGGLE_DATASET_PATH = config.KAGGLE_DATASET_PATH
KAGGLE_DATASET_NAME = config.KAGGLE_DATASET_NAME 