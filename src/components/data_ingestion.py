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
        
        # Fetch comments with pagination, but stop when we have 100 comments
        while request and len(comments) < 100:
            response = request.execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

                # Break if we've reached the desired number of comments
                if len(comments) >= 100:
                    break

            # Check if there's a next page and we haven't reached 100 comments yet
            if len(comments) < 100:
                request = youtube.commentThreads().list_next(request, response)

        logging.info(f"{len(comments)} comments fetched.")
        
        # Format comments as a numbered string
        formatted_comments = "\n".join([f"{i+1}. {comment}" for i, comment in enumerate(comments)])

        # Return formatted comments
        return formatted_comments

    except Exception as e:
        logging.error(f"Error fetching comments: {str(e)}")
        raise CustomException(e, sys)
