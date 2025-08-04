
import streamlit as st
import pandas as pd
import altair as alt
from src.streamlit_monitoring.data_loader import load_feedback_logs, load_imdb_dataset, load_all_logs
from src.utils import logger

st.set_page_config(page_title="Sentiment Model Monitoring", layout="wide")
logger.info("Streamlit monitoring app started.")

st.title("Sentiment Model Monitoring Dashboard")

if st.button("🔄 Refresh Data"):
    logger.info("'Refresh Data' button clicked.")
    st.rerun()

def load_data():
    try:
        logger.info("Loading all logs, feedback logs, and IMDB dataset.")
        all_logs = load_all_logs()
        feedback_logs = load_feedback_logs()
        imdb_df = load_imdb_dataset()
        logger.info("Data loading complete.")
        return all_logs, feedback_logs, imdb_df
    except Exception as e:
        logger.exception(f"Failed to load data for monitoring dashboard: {e}")
        st.error(f"Failed to load data: {e}")
        return [], [], pd.DataFrame()

all_logs, feedback_logs, imdb_df = load_data()

if not feedback_logs:
    st.warning("No feedback data found. Please add some feedback to see the monitoring dashboard.")
    logger.warning("No feedback data found for monitoring dashboard.")
else:
    st.header("Data Drift Analysis")
    
    # Data Drift Analysis
    imdb_sentence_lengths = imdb_df['review'].str.len()
    log_sentence_lengths = [len(log['request_text']) for log in all_logs]
    
    source = pd.DataFrame({
        'Sentence Length': imdb_sentence_lengths.tolist() + log_sentence_lengths,
        'Source': ['IMDB Dataset'] * len(imdb_sentence_lengths) + ['Inference Logs'] * len(log_sentence_lengths)
    })
    
    chart = alt.Chart(source).transform_density(
        'Sentence Length',
        as_=['Sentence Length', 'density'],
        groupby=['Source']
    ).mark_area(opacity=0.5).encode(
        x="Sentence Length:Q",
        y='density:Q',
        color='Source:N'
    ).properties(
        title='Distribution of Sentence Lengths'
    )
    
    st.altair_chart(chart, use_container_width=True)

    st.header("Target Drift Analysis")
    
    # Target Drift Analysis
    st.subheader("IMDB Dataset Sentiment Distribution")
    imdb_sentiments = imdb_df['sentiment'].value_counts().reset_index()
    imdb_sentiments.columns = ['Sentiment', 'Count']
    imdb_sentiments['Percentage'] = (imdb_sentiments['Count'] / imdb_sentiments['Count'].sum()) * 100

    imdb_bars = alt.Chart(imdb_sentiments).mark_bar().encode(
        x=alt.X('Sentiment:N', sort=['positive', 'negative']),
        y='Count:Q',
        tooltip=['Sentiment', 'Count', alt.Tooltip('Percentage:Q', format='.2f')]
    )

    imdb_text = imdb_bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3
    ).encode(
        y='Count:Q',
        text=alt.Text('Percentage:Q', format='.1f')
    )

    imdb_chart = (imdb_bars + imdb_text).properties(
        title='IMDB Dataset Sentiment Distribution'
    )
    st.altair_chart(imdb_chart, use_container_width=True)
    
    st.subheader("Inference Logs Sentiment Distribution")
    log_sentiments = pd.DataFrame([log['predicted_sentiment'] for log in all_logs], columns=['Sentiment'])
    log_sentiments = log_sentiments['Sentiment'].value_counts().reset_index()
    log_sentiments.columns = ['Sentiment', 'Count']
    log_sentiments['Percentage'] = (log_sentiments['Count'] / log_sentiments['Count'].sum()) * 100

    log_bars = alt.Chart(log_sentiments).mark_bar().encode(
        x=alt.X('Sentiment:N', sort=['positive', 'negative']),
        y='Count:Q',
        tooltip=['Sentiment', 'Count', alt.Tooltip('Percentage:Q', format='.2f')]
    )

    log_text = log_bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-3
    ).encode(
        y='Count:Q',
        text=alt.Text('Percentage:Q', format='.1f')
    )

    log_chart = (log_bars + log_text).properties(
        title='Inference Logs Sentiment Distribution'
    )
    st.altair_chart(log_chart, use_container_width=True)
    
    st.header("Model Accuracy & User Feedback")
    
    # Model Accuracy & User Feedback
    true_sentiments = [log['true_sentiment'] for log in feedback_logs]
    predicted_sentiments = [log['predicted_sentiment'] for log in feedback_logs]
    
    from sklearn.metrics import accuracy_score, precision_score
    
    accuracy = accuracy_score(true_sentiments, predicted_sentiments)
    precision = precision_score(true_sentiments, predicted_sentiments, pos_label='positive')
    
    col1, col2 = st.columns(2)
    col1.metric("Accuracy", f"{accuracy:.2f}")
    col2.metric("Precision", f"{precision:.2f}")
    
    st.header("Alerting")
    
    if accuracy < 0.8:
        st.error("Model accuracy has dropped below 80%!")
        logger.warning(f"Model accuracy has dropped to {accuracy:.2f}, which is below the 80% threshold.")
        logger.warning(f"Model precision is {precision:.2f}.")
    else:
        st.success("Model accuracy is above 80%.")
        logger.info(f"Model accuracy is {accuracy:.2f}, which is above the 80% threshold.")
        logger.info(f"Model precision is {precision:.2f}.")
    st.header("Raw Feedback Data")
    st.dataframe(pd.DataFrame(feedback_logs))
