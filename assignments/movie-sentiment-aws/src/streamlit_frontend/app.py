"""
Streamlit Frontend for Movie Sentiment Analysis

This application provides a user interface to interact with the
FastAPI sentiment analysis backend.
"""

import os
import requests
import streamlit as st
from src.core import logger

FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Movie Sentiment Analysis", layout="centered")
logger.info("Streamlit frontend app started.")

# Session state variables for ML monitoring
if "review_text" not in st.session_state:
    st.session_state.review_text = ""
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False


def handle_feedback(is_correct: bool):
    """
    Sends feedback to the backend.
    Args:
        is_correct (bool): Whether the feedback is correct.
        session_state (dict): The session state.
    """
    if st.session_state.prediction_result:
        predicted_sentiment = st.session_state.prediction_result["sentiment"]
        probability = st.session_state.prediction_result["probability"]

        if is_correct:
            true_sentiment = predicted_sentiment
        else:
            true_sentiment = "positive" if predicted_sentiment == "negative" else "negative"
            
        feedback_payload = {
            "request_text": st.session_state.review_text,
            "predicted_sentiment": predicted_sentiment,
            "probability": probability,
            "true_sentiment": true_sentiment,
            "is_sentiment_correct": is_correct,
        }
        try:
            logger.info(f"Submitting feedback: {feedback_payload}")
            requests.post(f"{FASTAPI_BACKEND_URL}/true_sentiment", json=feedback_payload)
            st.session_state.feedback_submitted = True
            st.toast("Thank you for your feedback!")
            logger.info("Feedback submitted successfully.")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not submit feedback: {e}")
            logger.error(f"Could not submit feedback to backend: {e}", exc_info=True)


st.title("Movie Sentiment Analysis")
st.markdown(
    "Enter a movie review below to predict its sentiment (positive or negative). "
    "This app sends a request to a FastAPI backend for the prediction."
)

st.subheader("Don't know what to write?")
if st.button("Get a Random Review Example"):
    logger.info("'Get a Random Review Example' button clicked.")
    try:
        response = requests.get(f"{FASTAPI_BACKEND_URL}/example")
        response.raise_for_status()
        example_review = response.json().get("review", "")
        st.session_state.review_text = example_review
        st.session_state.prediction_result = None
        st.session_state.feedback_submitted = False
        logger.info("Successfully fetched random review example.")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        st.warning("Please ensure the FastAPI backend service is running.")
        logger.error(f"Could not connect to backend for random review: {e}", exc_info=True)

review_text = st.text_area(
    "Enter your movie review here:",
    height=150,
    key="review_text",
    placeholder="I LOVE TRANSFORMERS. SHIA LA BEOUF IS THE BEST!",
)

if st.button("Analyze Sentiment"):
    logger.info("'Analyze Sentiment' button clicked.")
    if not st.session_state.review_text:
        st.warning("Please enter a review before analyzing.")
        logger.warning("Analyze sentiment called with no review text.")
    else:
        try:
            with st.spinner("Analyzing..."):
                payload = {"text": st.session_state.review_text}
                logger.info(f"Sending request to /predict_proba with payload: {{'text': '{st.session_state.review_text[:50]}...'}}")
                response = requests.post(
                    f"{FASTAPI_BACKEND_URL}/predict_proba", json=payload
                )
                response.raise_for_status()
                st.session_state.prediction_result = response.json()
                st.session_state.feedback_submitted = False
                logger.info(f"Received prediction: {st.session_state.prediction_result}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
            st.info(
                f"Please ensure the backend is running and accessible at `{FASTAPI_BACKEND_URL}`."
            )
            st.session_state.prediction_result = None
            logger.error(f"Error communicating with backend for prediction: {e}", exc_info=True)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state.prediction_result = None
            logger.exception(f"An unexpected error occurred during sentiment analysis: {e}")

if st.session_state.prediction_result:
    result = st.session_state.prediction_result
    sentiment = result.get("sentiment")
    probability = result.get("probability", 0)

    st.subheader("Analysis Result")
    if sentiment == "positive":
        logger.info(f"Displaying positive sentiment result with {probability * 100:.2f}% confidence")
        st.success(
            f"**Positive 👍** sentiment with a confidence of "
            f"**{probability * 100:.2f}%**"
        )
    elif sentiment == "negative":
        logger.info(f"Displaying negative sentiment result with {probability * 100:.2f}% confidence")
        st.error(
            f"**Negative 👎** sentiment with a confidence of "
            f"**{probability * 100:.2f}%**"
        )
    else:
        logger.warning("Could not determine sentiment from prediction result")
        st.warning("Could not determine the sentiment.")

    if not st.session_state.feedback_submitted:
        st.write("Was this prediction correct?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Correct ✅", on_click=handle_feedback, args=(True,), use_container_width=True):
                logger.info("User clicked 'Correct' feedback button")
        with col2:
            if st.button("Incorrect ❌", on_click=handle_feedback, args=(False,), use_container_width=True):
                logger.info("User clicked 'Incorrect' feedback button")

elif st.session_state.feedback_submitted:
    st.success("Thank you for your feedback!")


st.markdown("---")
st.markdown(
    "Built with Streamlit, FastAPI, and Scikit-learn. "
    f"Backend running at: `{FASTAPI_BACKEND_URL}`"
)
st.markdown(
    "🔗 [View source on GitHub](https://github.com/jairus-m/mlops-du)",
    unsafe_allow_html=True,
)
