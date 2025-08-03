"""
Streamlit Frontend for Movie Sentiment Analysis

This application provides a user interface to interact with the
FastAPI sentiment analysis backend.
"""

import os
import requests
import streamlit as st

FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Movie Sentiment Analysis", layout="centered")

# Session state variables for ML monitoring
if "review_text" not in st.session_state:
    st.session_state.review_text = ""
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False


def handle_feedback(is_correct: bool, session_state: dict):
    """
    Sends feedback to the backend.
    Args:
        is_correct (bool): Whether the feedback is correct.
        session_state (dict): The session state.
    """
    if session_state.prediction_result:
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
            requests.post(f"{FASTAPI_BACKEND_URL}/true_sentiment", json=feedback_payload)
            st.session_state.feedback_submitted = True
            st.toast("Thank you for your feedback!")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not submit feedback: {e}")


st.title("Movie Sentiment Analysis")
st.markdown(
    "Enter a movie review below to predict its sentiment (positive or negative). "
    "This app sends a request to a FastAPI backend for the prediction."
)

st.subheader("Don't know what to write?")
if st.button("Get a Random Review Example"):
    try:
        response = requests.get(f"{FASTAPI_BACKEND_URL}/example")
        response.raise_for_status()
        example_review = response.json().get("review", "")
        st.session_state.review_text = example_review
        st.session_state.prediction_result = None
        st.session_state.feedback_submitted = False
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        st.warning("Please ensure the FastAPI backend service is running.")

review_text = st.text_area(
    "Enter your movie review here:",
    height=150,
    key="review_text",
    placeholder="I LOVE TRANSFORMERS. SHIA LA BEOUF IS THE BEST!",
)

if st.button("Analyze Sentiment"):
    if not st.session_state.review_text:
        st.warning("Please enter a review before analyzing.")
    else:
        try:
            with st.spinner("Analyzing..."):
                payload = {"text": st.session_state.review_text}
                response = requests.post(
                    f"{FASTAPI_BACKEND_URL}/predict_proba", json=payload
                )
                response.raise_for_status()
                st.session_state.prediction_result = response.json()
                st.session_state.feedback_submitted = False

        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
            st.info(
                f"Please ensure the backend is running and accessible at `{FASTAPI_BACKEND_URL}`."
            )
            st.session_state.prediction_result = None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state.prediction_result = None

if st.session_state.prediction_result:
    result = st.session_state.prediction_result
    sentiment = result.get("sentiment")
    probability = result.get("probability", 0)

    st.subheader("Analysis Result")
    if sentiment == "positive":
        st.success(
            f"**Positive 👍** sentiment with a confidence of "
            f"**{probability * 100:.2f}%**"
        )
    elif sentiment == "negative":
        st.error(
            f"**Negative 👎** sentiment with a confidence of "
            f"**{probability * 100:.2f}%**"
        )
    else:
        st.warning("Could not determine the sentiment.")

    if not st.session_state.feedback_submitted:
        st.write("Was this prediction correct?")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Correct ✅", on_click=handle_feedback, args=(True,), use_container_width=True)
        with col2:
            st.button("Incorrect ❌", on_click=handle_feedback, args=(False,), use_container_width=True)

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
