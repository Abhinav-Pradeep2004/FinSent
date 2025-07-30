# src/utils/sentiment_analyzer.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.utils.news_fetcher import fetch_headlines_from_yahoo

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

def analyze_sentiment_multiple_stocks(stock_list, max_items=5):
    stock_sentiments = {}
    
    for ticker in stock_list:
        headlines = fetch_headlines_from_yahoo(ticker, max_items=max_items)

        # If headlines exist
        if headlines:
            positive, negative, neutral, compound_scores = [], [], [], []

            for headline in headlines:
                sentiment = analyzer.polarity_scores(headline)
                positive.append(sentiment['pos'])
                negative.append(sentiment['neg'])
                neutral.append(sentiment['neu'])
                compound_scores.append(sentiment['compound'])

            avg_score = round(sum(compound_scores) / len(compound_scores), 3)
            stock_sentiments[ticker] = {
                "positive": round(sum(positive) / len(positive), 3),
                "negative": round(sum(negative) / len(negative), 3),
                "neutral": round(sum(neutral) / len(neutral), 3),
                "score": avg_score
            }

        else:
            # Provide default sentiment when no headlines found
            stock_sentiments[ticker] = {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0,
                "score": 0.0
            }

    return stock_sentiments
