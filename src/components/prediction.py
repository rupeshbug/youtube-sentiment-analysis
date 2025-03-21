import os
import sys
from groq import Groq
import json

from src.logger import logging
from src.exception import CustomException

from src.utils import save_results_to_file

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def analyze_sentiments(comments, video_id):
    """
    Analyzes sentiments of the provided YouTube comments using Groq's LLM.

    Args:
        comments (list): List of YouTube comments.

    Returns:
        dict: A dictionary containing sentiment counts and top sentiment-related words/phrases.
    """
    try:
        # Prepare the system message and user message with the comments
        system_message = (
            "You are an AI that analyzes the sentiment of YouTube comments. "
            "Your task is to classify sentiments as Positive, Negative, or Neutral and identify "
            "the top sentiment-related phrases or words. Consider comments expressing admiration or respect as Positive or Neutral."
        )

        user_message = f"""Analyze the following comments and classify the sentiment as Positive, Neutral, or Negative.
        Then, return:
        1. The count of Positive, Neutral, and Negative sentiments.
        2. The **20 most frequently used words or phrases** that strongly indicate sentiment. Dont repeat them. (e.g., 'time waste', 'very good', 'not helpful').

        Comments:
        {json.dumps(comments, indent=2)}

        Format the response as a JSON object like this:
        {{
            "sentiment_counts": {{
                "positive": X,
                "neutral": Y,
                "negative": Z
            }},
            "top_sentiment_phrases": [
                "time waste",
                "very good",
                "not helpful",
                ...
            ]
        }}
        """
        
        # Send the request to the Groq model
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_message},
                      {"role": "user", "content": user_message}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False
        )

        logging.info("Sentiment Analysis by the model....")
        
        # Parse the response and extract sentiment counts and top phrases
        response_dict = json.loads(chat_completion.choices[0].message.content)
        
        sentiment_counts = response_dict["sentiment_counts"]
        top_sentiment_phrases = response_dict["top_sentiment_phrases"]
        
        logging.info("Results obtained")
        
        save_results_to_file(sentiment_counts, top_sentiment_phrases, video_id)

        return sentiment_counts, top_sentiment_phrases

    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
        raise CustomException(e, sys)
    