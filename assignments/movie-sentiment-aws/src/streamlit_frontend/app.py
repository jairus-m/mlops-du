import os
import requests
import streamlit as st


FASTAPI_URL = os.environ.get(
    "FASTAPI_URL", "http://127.0.0.1:8000/predict/"
)

st.title("Movie Review Sentiment Analyzer")
st.write(
    "This app analyzes the sentiment of movie reviews and predicts whether they are positive or negative."
)

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
        try:
            # The data to be sent in the POST request
            payload = {"text": user_text}
            
            # Make the POST request to the FastAPI backend
            response = requests.post(FASTAPI_URL, json=payload)
            
            # Check if the request was successful
            if response.status_code == 200:
                prediction_data = response.json()
                sentiment = prediction_data.get("sentiment", "N/A")
                
                st.subheader("Predicted Review Sentiment!")
                
                # Display the prediction in a styled box
                if sentiment == "positive":
                    st.success("Positive 👍")
                else:
                    st.error("Negative 👎")
                    
                # Try to get probability from predict_proba endpoint
                try:
                    proba_response = requests.post(
                        FASTAPI_URL.replace("/predict/", "/predict_proba"), 
                        json=payload
                    )
                    if proba_response.status_code == 200:
                        proba_data = proba_response.json()
                        probability = proba_data.get("probability", "N/A")
                        st.write(f"Confidence: {probability:.2%}")
                        
                        st.write("**Detailed Probabilities:**")
                        if sentiment == "positive":
                            st.write(f"- Positive: {probability:.2%}")
                            st.write(f"- Negative: {(1-probability):.2%}")
                        else:
                            st.write(f"- Negative: {probability:.2%}")
                            st.write(f"- Positive: {(1-probability):.2%}")
                except requests.exceptions.RequestException:
                    st.info("Probability information not available")
                    
            else:
                st.error(f"Error: Received status code {response.status_code}")
                st.json(response.json())

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend API. Please ensure it is running at {FASTAPI_URL}. Error: {e}")
