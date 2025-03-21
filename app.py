from flask import Flask, render_template, request
from src.components.data_ingestion import fetch_youtube_comments
from src.components.prediction import analyze_sentiments

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_id = request.form['video_id']
    comments = fetch_youtube_comments(video_id)
    sentiment_counts, top_sentiment_phrases = analyze_sentiments(comments, video_id)

    return render_template('results.html', 
                           sentiment_counts=sentiment_counts, 
                           top_sentiment_phrases=top_sentiment_phrases)

if __name__ == '__main__':
    app.run(debug=True)
