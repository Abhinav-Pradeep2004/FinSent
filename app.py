import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from src.utils.yfinance_fetcher import fetch_stock_data
from src.utils.sentiment_analyzer import analyze_news_sentiment, analyze_sentiment_multiple_stocks
from src.utils.news_fetcher import fetch_headlines_from_yahoo

# 📈 Title and description
st.set_page_config(page_title="FinSent – Stock Dashboard", layout="wide")
st.title("📈 FinSent – Stock Price Dashboard")
st.write("Track real-time stock prices and news sentiment analysis for top stocks.")

# 🔹 Stock options
stock_options = {
    # US Tech Giants
    'Apple (AAPL)': 'AAPL',
    'Google (GOOG)': 'GOOG',
    'Microsoft (MSFT)': 'MSFT',
    'Amazon (AMZN)': 'AMZN',
    'Tesla (TSLA)': 'TSLA',
    'Meta Platforms (META)': 'META',
    'NVIDIA (NVDA)': 'NVDA',
    'Netflix (NFLX)': 'NFLX',
    'Intel (INTC)': 'INTC',
    'Adobe (ADBE)': 'ADBE',
    'Oracle (ORCL)': 'ORCL',
    'AMD (AMD)': 'AMD',
    'Zoom Video (ZM)': 'ZM',
    'Salesforce (CRM)': 'CRM',
    'Uber (UBER)': 'UBER',

    # Indian IT & Tech
    'Infosys (INFY.NS)': 'INFY.NS',
    'TCS (TCS.NS)': 'TCS.NS',
    'Wipro (WIPRO.NS)': 'WIPRO.NS',
    'HCL Tech (HCLTECH.NS)': 'HCLTECH.NS',
    'Tech Mahindra (TECHM.NS)': 'TECHM.NS',
    'LTIMindtree (LTIM.NS)': 'LTIM.NS',

    # Indian Banks & Finance
    'HDFC Bank (HDFCBANK.NS)': 'HDFCBANK.NS',
    'ICICI Bank (ICICIBANK.NS)': 'ICICIBANK.NS',
    'State Bank of India (SBIN.NS)': 'SBIN.NS',
    'Axis Bank (AXISBANK.NS)': 'AXISBANK.NS',
    'Kotak Bank (KOTAKBANK.NS)': 'KOTAKBANK.NS',
    'Bajaj Finance (BAJFINANCE.NS)': 'BAJFINANCE.NS',
    'Bajaj Finserv (BAJAJFINSV.NS)': 'BAJAJFINSV.NS',

    # Indian FMCG & Consumer
    'Hindustan Unilever (HINDUNILVR.NS)': 'HINDUNILVR.NS',
    'ITC (ITC.NS)': 'ITC.NS',
    'Dabur (DABUR.NS)': 'DABUR.NS',
    'Nestle India (NESTLEIND.NS)': 'NESTLEIND.NS',
    'Britannia (BRITANNIA.NS)': 'BRITANNIA.NS',
    'Marico (MARICO.NS)': 'MARICO.NS',

    # Indian Energy & Industrial
    'Reliance Industries (RELIANCE.NS)': 'RELIANCE.NS',
    'L&T (LT.NS)': 'LT.NS',
    'Adani Enterprises (ADANIENT.NS)': 'ADANIENT.NS',
    'Adani Green (ADANIGREEN.NS)': 'ADANIGREEN.NS',
    'NTPC (NTPC.NS)': 'NTPC.NS',
    'ONGC (ONGC.NS)': 'ONGC.NS',
    'Power Grid Corp (POWERGRID.NS)': 'POWERGRID.NS',

    # Indian Automobiles
    'Tata Motors (TATAMOTORS.NS)': 'TATAMOTORS.NS',
    'Mahindra & Mahindra (M&M.NS)': 'M&M.NS',
    'Maruti Suzuki (MARUTI.NS)': 'MARUTI.NS',
    'Eicher Motors (EICHERMOT.NS)': 'EICHERMOT.NS',
    'Hero MotoCorp (HEROMOTOCO.NS)': 'HEROMOTOCO.NS',
    'Bajaj Auto (BAJAJ-AUTO.NS)': 'BAJAJ-AUTO.NS',
}

period_options = ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
interval_options = ["1d", "1h", "30m", "15m", "5m"]

# 🔹 Sidebar selections
st.sidebar.header("Select Options")
selected_stock = st.sidebar.selectbox("Select Stock", list(stock_options.keys()))
period = st.sidebar.selectbox("Select Period", period_options, index=1)
interval = st.sidebar.selectbox("Select Interval", interval_options, index=0)

# ⏳ Fetch button
if st.sidebar.button("🗓️ Fetch Data"):
    ticker = stock_options[selected_stock]
    df = fetch_stock_data(ticker, period, interval)

    if df is None or df.empty:
        st.error("Failed to fetch data. Try again.")
    else:
        st.success(f"Data fetched for {ticker}")

        # 🔍 Show table
        st.subheader("Recent Stock Data")
        st.dataframe(df.tail(10).reset_index(), use_container_width=True)

        # 🔢 Line Chart
        st.subheader("📊 Closing Price Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=ticker))
        fig.update_layout(title=f"Closing Prices of {ticker}", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

        # 🧠 News Sentiment
        st.subheader("🔍 News Sentiment Analysis")
        headlines = fetch_headlines_from_yahoo(ticker)

        if not headlines:
            st.warning("No recent news found.")
        else:
            sentiment_results = analyze_news_sentiment(headlines)
            for item in sentiment_results:
                color = ("green" if item['sentiment'] == "Positive" else
                         "red" if item['sentiment'] == "Negative" else
                         "gray")
                st.markdown(f"<span style='color:{color}'>{item['headline']} → {item['sentiment']} ({item['score']})</span>", unsafe_allow_html=True)

# 🔹 Optional: Show stock-wise sentiment comparison chart
st.subheader("📊 Stock-wise Sentiment Graph (Top 5 Selections)")
selected_top5 = st.multiselect("Compare Multiple Stocks", list(stock_options.keys()), max_selections=5)

if selected_top5:
    tickers = [stock_options[label] for label in selected_top5]

    # Run sentiment analysis
    sentiment_data = analyze_sentiment_multiple_stocks(tickers)

    # Get stock names
    stock_names = list(sentiment_data.keys())

    # Debug print for missing sentiment keys
    for s in stock_names:
        if 'positive' not in sentiment_data[s] or \
           'negative' not in sentiment_data[s] or \
           'neutral' not in sentiment_data[s]:
            st.warning(f"Missing sentiment keys for stock: {s}")
            st.json(sentiment_data[s])

    # Safely access sentiment scores with defaults
    positive_scores = [sentiment_data[s].get('positive', 0) for s in stock_names]
    negative_scores = [sentiment_data[s].get('negative', 0) for s in stock_names]
    neutral_scores  = [sentiment_data[s].get('neutral', 0) for s in stock_names]

    # Now use these scores for charting or display
    # For example, a bar chart using Plotly or Streamlit's st.bar_chart


    fig_bar = go.Figure(data=[
        go.Bar(x=stock_names, y=positive_scores, name="Positive", marker_color='green'),
        go.Bar(x=stock_names, y=negative_scores, name="Negative", marker_color='red'),
        go.Bar(x=stock_names, y=neutral_scores, name="Neutral", marker_color='gray'),
    ])

    fig_bar.update_layout(
        title="Stock-wise Sentiment Analysis",
        barmode='stack',
        xaxis_title="Stocks",
        yaxis_title="Sentiment Score",
        template="plotly_white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
