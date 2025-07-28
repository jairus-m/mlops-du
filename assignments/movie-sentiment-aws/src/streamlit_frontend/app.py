"""
Streamlit Frontend for Movie Sentiment Analysis

This application provides a user interface to interact with the
FastAPI sentiment analysis backend.
"""

import os
import requests
import streamlit as st

# --- Configuration ---
# Get the backend URL from an environment variable.
# Fallback to a local default for easy development.
API_BACKEND_URL = os.getenv("API_BACKEND_URL", "http://localhost:8000")

# --- App Layout ---
st.set_page_config(page_title="Movie Sentiment Analysis", layout="centered")

st.title("🎬 Movie Sentiment Analysis")
st.markdown(
    "Enter a movie review below to predict its sentiment (positive or negative). "
    "This app sends a request to a FastAPI backend for the prediction."
)

# --- Example Review ---
st.subheader("Don't know what to write?")
if st.button("Get a Random Review Example"):
    try:
        response = requests.get(f"{API_BACKEND_URL}/example")
        response.raise_for_status()  # Raise an exception for bad status codes
        example_review = response.json().get("review", "")
        st.session_state.review_text = example_review
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
        st.warning("Please ensure the FastAPI backend service is running.")

# --- User Input ---
review_text = st.text_area(
    "Enter your movie review here:",
    height=150,
    key="review_text",
    placeholder="I loved this movie, the acting was superb!",
)

# --- Prediction ---
if st.button("Analyze Sentiment"):
    if not review_text:
        st.warning("Please enter a review before analyzing.")
    else:
        try:
            with st.spinner("Analyzing..."):
                # The data to be sent in the POST request
                payload = {"text": review_text}

                # Make a single API call to the more informative endpoint
                response = requests.post(
                    f"{API_BACKEND_URL}/predict_proba", json=payload
                )
                response.raise_for_status()  # Raise an exception for bad status codes
                result = response.json()

                sentiment = result.get("sentiment")
                probability = result.get("probability", 0)

                # Display the result
                st.subheader("Analysis Result")
                if sentiment == "positive":
                    st.success(
                        f"**Positive 👍** sentiment with a confidence of "
                        f"**{probability*100:.2f}%**"
                    )
                elif sentiment == "negative":
                    st.error(
                        f"**Negative 👎** sentiment with a confidence of "
                        f"**{probability*100:.2f}%**"
                    )
                else:
                    st.warning("Could not determine the sentiment.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
            st.info(
                f"Please ensure the backend is running and accessible at `{API_BACKEND_URL}`."
            )
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- Footer ---
st.markdown("---")
st.markdown(
    "Built with Streamlit, FastAPI, and Scikit-learn. "
    f"Backend running at: `{API_BACKEND_URL}`"
)
