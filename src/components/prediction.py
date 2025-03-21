import os
import sys
from groq import Groq
import json
import re

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
            "the top sentiment-related phrases or words (e.g., 'time waste', 'very good', 'not helpful')."
            "You must strictly return only the requested JSON object without any extra explanations or text."
            
        )

        user_message = f"""Analyze the following comments and classify the sentiment as Positive, Neutral, or Negative.
        Then, return:
        1. The count of Positive, Neutral, and Negative sentiments.
        2. The **10 most frequently used sentiment-related phrases** that strongly indicate sentiment (e.g., 'time waste', 'very good', 'not helpful').

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

        # Log the raw response for debugging
        logging.info("Result Saved....")
        
        # Extract the JSON part of the response using regex
        match = re.search(r'(\{.*\})', chat_completion.choices[0].message.content, re.DOTALL)
        
        if not match:
            logging.error("Failed to find valid JSON in the response.")
            raise CustomException("Failed to extract valid JSON from Groq response", sys)
        
        # Parse the valid JSON
        response_dict = json.loads(match.group(1))
        
        sentiment_counts = response_dict.get("sentiment_counts", {})
        top_sentiment_phrases = response_dict.get("top_sentiment_phrases", [])

        if not sentiment_counts or not top_sentiment_phrases:
            logging.error("Invalid response: Missing sentiment counts or top phrases.")
            raise CustomException("Groq response is missing sentiment counts or phrases", sys)

        logging.info("Results obtained")
        
        # Save results to file
        save_results_to_file(sentiment_counts, top_sentiment_phrases, video_id)

        return sentiment_counts, top_sentiment_phrases

    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
        raise CustomException(e, sys)
