import streamlit as st
import joblib
from sklearn.pipeline import Pipeline
from src.utils import MODEL_PATH

st.title("Movie Review Sentiment Analyzer")
st.write(
    "This app analyzes the sentiment of movie reviews and predicts whether they are positive or negative."
)


@st.cache_data
def load_model(model_path: str) -> Pipeline:
    """
    Load the sentiment analysis model with caching for performance.
    Args:
        model_path (str): Path to the model file
    Returns:
        model (Pipeline): The loaded model
    """
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {model_path}")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


model = load_model(MODEL_PATH)

if model is None:
    st.stop()

# GUI for user input
st.subheader("Enter a movie review to analyze:")
user_text = st.text_area(
    label="Movie Review",
    placeholder="Type or paste your movie review here...",
    height=150,
)

analyze_button = st.button("Analyze")

# Make Predictions and Display Results
if analyze_button:
    if user_text.strip() == "":
        st.warning("Please enter a movie review before analyzing.")
    else:
        prediction = model.predict([user_text])[0]
        # st.write("Debug - Raw prediction:", prediction)

        probabilities = model.predict_proba([user_text])[0]
        # st.write("Debug - Raw probabilities:", probabilities)

        st.subheader("Predicted Review Sentiment!")

        if prediction == 1:
            st.success("Positive 👍")
            st.write(f"Confidence: {probabilities[1]:.2%}")
        else:
            st.error("Negative 👎")
            st.write(f"Confidence: {probabilities[0]:.2%}")

        st.write("**Detailed Probabilities:**")
        st.write(f"- Negative: {probabilities[0]:.2%}")
        st.write(f"- Positive: {probabilities[1]:.2%}")
