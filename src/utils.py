import os
import sys
import json

from src.logger import logging
from src.exception import CustomException

def save_results_to_file(sentiment_counts, top_sentiment_phrases, video_id):
    """
    Save sentiment analysis results to a file.
    
    Args:
        sentiment_counts (dict): Sentiment counts for the analysis.
        top_sentiment_phrases (list): List of top sentiment-related phrases.
        video_id (str): The ID of the YouTube video.
    """
    try:
        # Ensure the artifacts folder exists
        if not os.path.exists("data"):
            os.makedirs("data")

        result = {
            "sentiment_counts": sentiment_counts,
            "top_sentiment_phrases": top_sentiment_phrases
        }

        # Save to a JSON file with the video ID as filename
        result_filename = os.path.join("data", f"{video_id}_sentiment_analysis.json")
        
        with open(result_filename, "w") as f:
            json.dump(result, f, indent=4)

        logging.info(f"Sentiment analysis results saved to {result_filename}")
    except Exception as e:
        logging.error(f"Error saving results to file: {e}")
        raise CustomException(e, sys)
