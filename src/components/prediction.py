import os
import sys
from groq import Groq
import json

from src.logger import logging
from src.exception import CustomException

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def analyze_sentiments(comments):
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

        # Format comments for the prompt, without using json.dumps
        formatted_comments = "\n".join([f"{i + 1}. {comment}" for i, comment in enumerate(comments)])

        user_message = f"""Analyze the following comments and classify the sentiment as Positive, Neutral, or Negative.
        Then, return:
        1. The count of Positive, Neutral, and Negative sentiments.
        2. The **20 most frequently used words or phrases** that strongly indicate sentiment. Don't repeat them. (e.g., 'time waste', 'very good', 'not helpful').

        Comments:
        {formatted_comments}

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
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False
        )

        logging.info("Sentiment Analysis by the model....")
        
        # Parse the response and extract sentiment counts and top phrases
        response = json.loads(chat_completion.choices[0].message.content)

        sentiment_counts = response.get("sentiment_counts", {})
        top_sentiment_phrases = response.get("top_sentiment_phrases", [])
        
        logging.info("Results obtained")

        return sentiment_counts, top_sentiment_phrases

    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
        raise CustomException(e, sys)
