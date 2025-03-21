from flask import Flask, render_template, request
from src.components.data_ingestion import fetch_youtube_comments
from src.components.prediction import analyze_sentiments

import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_id = request.form['video_id']
    comments = fetch_youtube_comments(video_id)
    sentiment_counts, top_sentiment_phrases = analyze_sentiments(comments, video_id)
    
    # Create Pie Chart and Word Cloud
    pie_chart = create_pie_chart(sentiment_counts)
    word_cloud = create_word_cloud(top_sentiment_phrases)
    
    return render_template('results.html', 
                           sentiment_counts=sentiment_counts, 
                           top_sentiment_phrases=top_sentiment_phrases,
                           pie_chart=pie_chart, word_cloud=word_cloud)
    
def create_pie_chart(sentiment_counts):
    fig = px.pie(
        names=['Positive', 'Neutral', 'Negative'],
        values=[sentiment_counts['positive'], sentiment_counts['neutral'], sentiment_counts['negative']],
        title="Sentiment Distribution"
    )
    return fig.to_html(full_html=False)

def create_word_cloud(phrases):
    # Join phrases into a single string for WordCloud
    text = ' '.join(phrases)  # No need for .keys(), just join the list

    # Generate the word cloud
    wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(text)

    # Save the word cloud to a BytesIO object
    img = io.BytesIO()
    wc.to_image().save(img, format='PNG')
    img.seek(0)

    # Convert the image to base64 to embed it in HTML
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"

if __name__ == '__main__':
    app.run(debug=True)
