# src/utils/news_fetcher.py

import feedparser

def fetch_headlines_from_yahoo(ticker, max_items=5):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        feed = feedparser.parse(url)
        headlines = [entry.title for entry in feed.entries[:max_items]]
        return headlines
    except Exception as e:
        print(f"Error fetching RSS news for {ticker}: {e}")
        return []
