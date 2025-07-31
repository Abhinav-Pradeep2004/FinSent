import streamlit as st
import base64
from PIL import Image
import pandas as pd
import plotly.graph_objs as go
from src.utils.yfinance_fetcher import fetch_stock_data
from src.utils.sentiment_analyzer import analyze_news_sentiment, analyze_sentiment_multiple_stocks
from src.utils.news_fetcher import fetch_headlines_from_yahoo

# 🔧 Page config
st.set_page_config(page_title="FinSent – Stock Dashboard",page_icon="assest/favicon-removebg-preview.png", layout="wide")

def get_image_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Top-right logo
falcons_logo = get_image_as_base64("assest/falcons.png")

st.markdown(
    f"""
    <div style="position: fixed; top: 50px; right: 25px; z-index: 999;">
        <img src="data:image/png;base64,{falcons_logo}" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

# --- Header section (left logo + title)
col_logo, col_title = st.columns([2, 10])
with col_logo:
    st.image("assest/logo.png", width=350)

with col_title:
    st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 100px;'>
            <h1 style='margin-bottom: 0;'>Stock Analytics Dashboard</h1>
            <p style='margin-top: 5px; font-size: 16px; color: #cbd5e0;'>
                Track live stock prices and news sentiment analysis across multiple sectors.
            </p>
        </div>
    """, unsafe_allow_html=True)



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

# ----------------------
# 🚀 TABS for UI Layout
# ----------------------
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 50px ;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📉 Single Stock Explorer", "🧠 News Sentiment", "📊 Multi-Stock Comparison"])



# ----------------------
# 📉 Tab 1: Single Stock Explorer
# ----------------------
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_stock = st.selectbox("Choose Stock", list(stock_options.keys()))
    with col2:
        period = st.selectbox("Period", period_options, index=1)
    with col3:
        interval = st.selectbox("Interval", interval_options, index=0)

    if st.button("🔄 Fetch Stock Data"):
        ticker = stock_options[selected_stock]
        df = fetch_stock_data(ticker, period, interval)

        if df is None or df.empty:
            st.error("Failed to fetch stock data. Try again.")
        else:
            st.success(f"Showing data for {ticker}")

            st.subheader("📑 Latest Stock Data")
            st.dataframe(df.tail(10).reset_index(), use_container_width=True)

            st.subheader("📈 Closing Price Trend")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=ticker))
            fig.update_layout(title=f"{ticker} Closing Prices", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)

# ----------------------
# 🧠 Tab 2: News Sentiment
# ----------------------
with tab2:
    st.subheader("🔍 News-Based Sentiment Analysis")
    selected_sent_stock = st.selectbox("Select Stock for Sentiment", list(stock_options.keys()), key="sentiment_selector")
    ticker = stock_options[selected_sent_stock]

    if st.button("🧠 Analyze News Sentiment"):
        headlines = fetch_headlines_from_yahoo(ticker)

        if not headlines:
            st.warning("No recent headlines found.")
        else:
            sentiment_results = analyze_news_sentiment(headlines)
            for item in sentiment_results:
                color = ("green" if item['sentiment'] == "Positive" else
                         "red" if item['sentiment'] == "Negative" else
                         "gray")
                st.markdown(f"<span style='color:{color}'>{item['headline']} → {item['sentiment']} ({item['score']})</span>", unsafe_allow_html=True)

# ----------------------
# 📊 Tab 3: Multi-stock Sentiment Chart
# ----------------------
with tab3:
    st.subheader("📊 Stock-wise Sentiment Comparison (Top 5)")
    selected_top5 = st.multiselect("Select up to 5 Stocks", list(stock_options.keys()), max_selections=5)

    if selected_top5:
        tickers = [stock_options[label] for label in selected_top5]
        sentiment_data = analyze_sentiment_multiple_stocks(tickers)

        stock_names = list(sentiment_data.keys())
        for s in stock_names:
            if 'positive' not in sentiment_data[s] or \
               'negative' not in sentiment_data[s] or \
               'neutral' not in sentiment_data[s]:
                st.warning(f"Missing sentiment keys for: {s}")
                st.json(sentiment_data[s])

        positive_scores = [sentiment_data[s].get('positive', 0) for s in stock_names]
        negative_scores = [sentiment_data[s].get('negative', 0) for s in stock_names]
        neutral_scores  = [sentiment_data[s].get('neutral', 0) for s in stock_names]

        fig_line = go.Figure()

        fig_line.add_trace(go.Scatter(x=stock_names, y=positive_scores, mode='lines+markers', name='Positive', line=dict(color='green')))
        fig_line.add_trace(go.Scatter(x=stock_names, y=negative_scores, mode='lines+markers', name='Negative', line=dict(color='red')))
        fig_line.add_trace(go.Scatter(x=stock_names, y=neutral_scores, mode='lines+markers', name='Neutral', line=dict(color='gray')))

        fig_line.update_layout(
            title="Sentiment Comparison Across Stocks",
            xaxis_title="Stock",
            yaxis_title="Sentiment Score",
            template="plotly_white"
        )

        st.plotly_chart(fig_line, use_container_width=True)
