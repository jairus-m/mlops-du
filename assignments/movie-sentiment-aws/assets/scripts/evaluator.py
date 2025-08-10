import requests
import json
import os

FASTAPI_URL = "http://localhost:8000/predict"

def evaluate_api():
    """
    Evaluates the sentiment analysis API by using the test data in `assets/data/test.json`
    from Assignment 5.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(script_dir, "..", "data", "test.json")

    try:
        with open(test_data_path, "r") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {test_data_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {test_data_path}.")
        return

    url = FASTAPI_URL


    correct_predictions = 0
    total_predictions = len(test_data)

    for item in test_data:
        text = item.get("text")
        true_label = item.get("true_label")

        if not text or not true_label:
            print(f"Skipping invalid item: {item}")
            continue
    
        try:
            response = requests.post(url, json={"text": text})
            response.raise_for_status()
            predicted_sentiment = response.json().get("sentiment")

            if predicted_sentiment == true_label:
                correct_predictions += 1
        except requests.exceptions.RequestException as e:
            print(f"Error sending request for text: '{text}'. Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    if total_predictions > 0:
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"Accuracy: {accuracy:.2f}% ({correct_predictions}/{total_predictions})")
    else:
        print("No test data found to evaluate.")

if __name__ == "__main__":
    evaluate_api()
