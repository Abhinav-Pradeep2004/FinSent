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
    for stock in stock_list:
        ticker = stock
        label = stock  # You can replace this with a mapping to full names if available
        headlines = fetch_headlines_from_yahoo(ticker, max_items=max_items)
        if headlines:
            scores = [analyzer.polarity_scores(h)['compound'] for h in headlines]
            avg_score = round(sum(scores) / len(scores), 3) if scores else 0.0
        else:
            avg_score = 0.0
        stock_sentiments[ticker] = {'label': label, 'score': avg_score}
    return stock_sentiments

