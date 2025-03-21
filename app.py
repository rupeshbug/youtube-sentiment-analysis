from src.components.data_ingestion import fetch_youtube_comments
from src.components.prediction import analyze_sentiments

video_id = "6OofHvGJ-kM"
comments = fetch_youtube_comments(video_id)
results = analyze_sentiments(comments, video_id)
print(results)