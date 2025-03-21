from src.components.data_ingestion import fetch_youtube_comments

comments = fetch_youtube_comments("Y-M3CrPzI5A")
comments_str = "\n".join([f"{i+1}. {comment}" for i, comment in enumerate(comments)])
print(comments_str)