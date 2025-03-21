import os
import sys
from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.logger import logging
from src.exception import CustomException

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_comments(video_id):
    """
    Fetches comments from a YouTube video using the YouTube Data API.

    Limitations:
    - The API has request limits, so we fetch a maximum of 100 comments.
    - If a video has fewer comments, it will return all available comments.
    
    Args:
        video_id (str): The ID of the YouTube video.
    """
    logging.info("Entered Data Ingestion.")
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
    
        comments = []
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100 
        )
        
        response = request.execute()
        
        # Check if there are comments in the response
        if "items" in response:
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
            logging.info(f"{len(comments)} comments fetched.")
        else:
            logging.warning("No comments found for the given video.")
            
        return comments
    except Exception as e:
        logging.error(f"Error fetching comments: {str(e)}")
        raise CustomException(e, sys)
