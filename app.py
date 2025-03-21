from src.components.data_ingestion import fetch_youtube_comments
from src.components.prediction import analyze_sentiments

comments = fetch_youtube_comments("Y-M3CrPzI5A")
results = analyze_sentiments(comments)
print(results)