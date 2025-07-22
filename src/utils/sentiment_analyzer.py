# src/utils/sentiment_analyzer.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_news_sentiment(news_headlines):
    results = []
    for headline in news_headlines:
        score = analyzer.polarity_scores(headline)['compound']
        results.append({
            'headline': headline,
            'score': round(score, 3),
            'sentiment': (
                'Positive' if score > 0.05 else
                'Negative' if score < -0.05 else
                'Neutral'
            )
        })
    return results
