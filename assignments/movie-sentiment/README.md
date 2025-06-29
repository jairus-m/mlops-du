# Movie Review Sentiment Analyzer

An ML app that analyzes movie reviews and predicts whether they're positive or negative. This project uses a Naive Bayes classifier trained on the IMDB dataset to provide real-time sentiment analysis/inference through a Streamlit web UI.

## Project Structure

```
movie-sentiment/
├── assets/
│   ├── data/                       # Dataset directory
│   ├── docs/                       # Documentation
│   ├── images/                     # Image assets
│   └── models/
│       └── sentiment_model.pkl     # Trained model file
├── src/
│   ├── train/
│   │   └── train_model.py          # Model training script
│   ├── streamlit/
│   │   └── app.py                  # Streamlit web app
│   ├── utils/                      # Utils (logging) and constants
│   └── main.py                     # Main entry point to run ML training/streamlit app
├── pyproject.toml                  # Python dependencies
├── README.md                       # Submission docs 
└── uv.lock                         # uv lockfile for deps
```

## Installation and Setup 

### Clone the Repository and Install Dependencies

```bash
git clone https://github.com/jairus-m/mlops-du.git
cd mlops-du
bash install-tools.sh
```

### Run 
```bash
# Run from the mono repo root dir, mlops-du/
task movie-sentiment
```

**Run Notes:** 
- Running `task` will automatically download the IMDB data, train the ML model, and will open the Streamlit web app in `http://localhost:8501`
  - The dataset will be downloaded from [IMDB Dataset of 50K Movie Reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) and placed in the `assets/data` directory.
- Once in the Streamlit UI, enter a movie review in the text area and click "Analyze" to get sentiment predictions!

Run the following to manually execute the ML training script and to launch the Streamlit app:
```bash
cd assignments/movie-sentiment
uv sync
uv run python -m src.train.train_model
uv run streamlit run src/streamlit/app.py 
```

## Example Output
__Positive Sentiment:__  
<img src="assets/images/positive_sentiment.png" width="500"/>

__Negative Sentiment:__  
<img src="assets/images/negative_sentiment.png" width="500"/>
