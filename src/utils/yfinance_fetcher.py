# src/utils/yfinance_fetcher.py

import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker_symbol="RELIANCE.NS", period="1mo", interval="1d"):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            raise ValueError("No data found.")

        os.makedirs("data", exist_ok=True)
        hist.to_csv("data/stock_data.csv")

        return hist
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
