from unittest.mock import patch, MagicMock


def test_streamlit_monitoring_import():
    """Test that the streamlit monitoring module can be imported"""
    with (
        patch("pandas.read_csv", return_value=MagicMock()),
        patch(
            "src.streamlit_monitoring.utils.data_loader.load_all_logs", return_value=[]
        ),
        patch(
            "src.streamlit_monitoring.utils.data_loader.load_feedback_logs",
            return_value=[],
        ),
        patch(
            "src.streamlit_monitoring.utils.data_loader.load_imdb_dataset",
            return_value=MagicMock(),
        ),
    ):
        import src.streamlit_monitoring.app

        assert src.streamlit_monitoring.app is not None
