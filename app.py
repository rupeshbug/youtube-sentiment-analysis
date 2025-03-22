from flask import Flask, render_template, request,jsonify
from flask_cors import CORS
from src.components.data_ingestion import fetch_youtube_comments
from src.components.prediction import analyze_sentiments

import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "chrome-extension://gmgobhjnnannnbgkfffocgabcjnkcacf"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Parse the incoming JSON data
        data = request.get_json()
        video_id = data['video_id']
        
        # Fetch YouTube comments and analyze sentiments
        comments = fetch_youtube_comments(video_id)
        sentiment_counts, top_sentiment_phrases = analyze_sentiments(comments, video_id)
        
        # Get the sentiment counts for the pie chart
        pie_chart_data = create_pie_chart(sentiment_counts)
        word_cloud_url = create_word_cloud(top_sentiment_phrases)  # Same for the word cloud image
        
        # Prepare the response data as a JSON object
        response_data = {
            'status': "success",
            'sentiment_counts': sentiment_counts,
            'top_sentiment_phrases': top_sentiment_phrases,
            'pie_chart_data': { 
                'positive': sentiment_counts['positive'],
                'neutral': sentiment_counts['neutral'],
                'negative': sentiment_counts['negative']
            },
            'word_cloud_url': word_cloud_url
        }
        # Return JSON response
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def create_pie_chart(sentiment_counts):
    return {
        'positive': sentiment_counts['positive'],
        'neutral': sentiment_counts['neutral'],
        'negative': sentiment_counts['negative']
    }

def create_word_cloud(phrases):
    text = ' '.join(phrases)

    wc = WordCloud(width=300, height=250, background_color='white', max_words=100).generate(text)

    # Save the word cloud to a BytesIO object
    img = io.BytesIO()
    wc.to_image().save(img, format='PNG')
    img.seek(0)

    # Convert the image to base64 to embed it in HTML
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"

if __name__ == '__main__':
    app.run(debug=True)
