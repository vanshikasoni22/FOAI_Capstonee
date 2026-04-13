import pandas as pd
from datetime import datetime
import os

UNANSWERED_PATH = os.path.join(os.path.dirname(__file__), "../data/unanswered.csv")
FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), "../data/feedback.csv")

def log_unanswered(query):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[timestamp, query]], columns=["timestamp", "query"])
    new_row.to_csv(UNANSWERED_PATH, mode='a', header=False, index=False)

def log_feedback(rating, comment, sentiment_score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # sentiment_score is passed from VADER analysis in frontend
    new_row = pd.DataFrame([[timestamp, rating, comment, sentiment_score]], 
                           columns=["timestamp", "rating", "comment", "sentiment"])
    new_row.to_csv(FEEDBACK_PATH, mode='a', header=False, index=False)
