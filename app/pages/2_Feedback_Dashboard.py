import streamlit as st
import pandas as pd
import plotly.express as px
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Feedback Dashboard", layout="wide")

st.title("📊 Feedback & Sentiment Dashboard")

feedback_path = os.path.join(os.path.dirname(__file__), "../../data/feedback.csv")

if os.path.exists(feedback_path) and os.path.getsize(feedback_path) > 30: # Check if not empty
    df = pd.read_csv(feedback_path)
    
    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    
    def get_sentiment(text):
        if pd.isna(text) or text == "": return "Neutral"
        score = analyzer.polarity_scores(str(text))['compound']
        if score >= 0.05: return "Positive"
        elif score <= -0.05: return "Negative"
        else: return "Neutral"
        
    df['sentiment_label'] = df['comment'].apply(get_sentiment)
    
    # Summary Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Feedback", len(df))
    col2.metric("Avg Rating", round(df['rating'].mean(), 2) if 'rating' in df.columns else "N/A")
    pos_perc = (len(df[df['sentiment_label'] == "Positive"]) / len(df) * 100) if len(df) > 0 else 0
    col3.metric("% Positive", f"{round(pos_perc)}%")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Sentiment Distribution")
        fig_pie = px.pie(df, names='sentiment_label', color='sentiment_label',
                         color_discrete_map={'Positive':'#4ade80', 'Neutral':'#94a3b8', 'Negative':'#f87171'})
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Feedback Timeline")
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_rating = df.groupby('date')['rating'].mean().reset_index()
        fig_bar = px.bar(daily_rating, x='date', y='rating', color_discrete_sequence=['#38bdf8'])
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.subheader("All Feedback")
    st.dataframe(df[['timestamp', 'rating', 'comment', 'sentiment_label']], use_container_width=True)

else:
    st.info("No feedback data available yet. Please interact with the chatbot to generate data.")
    
    # Dummy data for preview if user wants to see UI
    if st.checkbox("Show Sample Dashboard"):
        sample_data = {
            'timestamp': ['2024-10-01', '2024-10-01', '2024-10-02'],
            'rating': [5, 4, 2],
            'comment': ['Excellent bot!', 'Very helpful', 'Didn\'t know about my scholarship'],
            'sentiment_label': ['Positive', 'Positive', 'Negative']
        }
        df_sample = pd.DataFrame(sample_data)
        st.header("Sample View")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df_sample, names='sentiment_label'), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df_sample, x='timestamp', y='rating'), use_container_width=True)
