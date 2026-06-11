from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)
analyzer = SentimentIntensityAnalyzer()

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    text = data.get('message', '')
    
    if not text:
        return jsonify({'error': 'No message provided'}), 400
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
    
    return jsonify({'sentiment': label})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
