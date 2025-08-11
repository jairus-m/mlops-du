import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from src.sklearn_training import train_model


@patch("src.sklearn_training.train_model.download_kaggle_dataset")
@patch("src.sklearn_training.train_model.load_and_preprocess_data")
@patch("src.sklearn_training.train_model.create_and_train_model_pipeline")
@patch("src.sklearn_training.train_model.save_model")
def test_run_training_smoke(
    mock_save_model,
    mock_create_and_train_model_pipeline,
    mock_load_and_preprocess_data,
    mock_download_kaggle_dataset,
):
    """
    Smoke test for the main training function to ensure it runs without errors.
    """
    # Mock return values
    mock_download_kaggle_dataset.return_value = "dummy_path.csv"
    mock_load_and_preprocess_data.return_value = (np.array(["a"]), np.array([1]))
    mock_create_and_train_model_pipeline.return_value = MagicMock()

    try:
        train_model.run_training()
    except Exception as e:
        pytest.fail(f"run_training() raised an exception: {e}")

    # Assert that the main functions were called
    mock_download_kaggle_dataset.assert_called_once()
    mock_load_and_preprocess_data.assert_called_once_with("dummy_path.csv")
    mock_create_and_train_model_pipeline.assert_called_once()
    mock_save_model.assert_called_once()
