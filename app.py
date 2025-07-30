import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.graph_objs as go
from src.utils.yfinance_fetcher import fetch_stock_data
from src.utils.news_fetcher import fetch_headlines_from_yahoo
from src.utils.sentiment_analyzer import analyze_news_sentiment, analyze_sentiment_multiple_stocks
app = dash.Dash(__name__)
server = app.server

# Stock options with label and value
stock_options = [
    {'label': 'Apple (AAPL)', 'value': 'AAPL'},
    {'label': 'Reliance (RELIANCE.NS)', 'value': 'RELIANCE.NS'},
    {'label': 'Infosys (INFY.NS)', 'value': 'INFY.NS'},
    {'label': 'TCS (TCS.NS)', 'value': 'TCS.NS'},
    {'label': 'Google (GOOG)', 'value': 'GOOG'},
    {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
    {'label': 'Amazon (AMZN)', 'value': 'AMZN'}
]

app.layout = html.Div([
    html.H1("Finsent - Stock Sentiment Analyzer"),

    dcc.Dropdown(
        id='stock-dropdown',
        options=stock_options,
        multi=True,
        value=['AAPL', 'RELIANCE.NS'],
        placeholder="Select stock(s)"
    ),

    html.Br(),
    html.H2("Stock-wise Sentiment Scores"),
    dcc.Graph(id='sentiment-bar-chart'),

    html.Br(),
    html.H2("Latest News & Individual Sentiment"),
    html.Div(id='individual-sentiment-output')
])

@app.callback(
    [Output('sentiment-bar-chart', 'figure'),
     Output('individual-sentiment-output', 'children')],
    Input('stock-dropdown', 'value')
)
def update_sentiment_graph(selected_stocks):
    if not selected_stocks:
        return go.Figure(), ""

    sentiment_data = analyze_sentiment_multiple_stocks(selected_stocks)

    bar_fig = go.Figure([
        go.Bar(
            x=[d['label'] for d in sentiment_data],
            y=[d['score'] for d in sentiment_data],
            marker_color='indianred'
        )
    ])

    bar_fig.update_layout(
        title='Average Sentiment Score per Stock',
        xaxis_title='Stock',
        yaxis_title='Sentiment Score',
        yaxis=dict(range=[-1, 1])
    )

    # Show recent headlines and sentiment
    sentiment_divs = []
    for d in sentiment_data:
        headlines = fetch_headlines_from_yahoo(d['ticker'])
        sentiment_results = analyze_news_sentiment(headlines)

        sentiment_divs.append(html.Div([
            html.H4(d['label'], style={'marginTop': '20px'}),
            html.Ul([
                html.Li(f"{item['headline']} → {item['sentiment']} ({item['score']})",
                        style={"color": "green" if item['sentiment'] == "Positive"
                               else "red" if item['sentiment'] == "Negative"
                               else "gray"})
                for item in sentiment_results
            ])
        ]))

    return bar_fig, html.Div(sentiment_divs)

if __name__ == '__main__':
    app.run_server(debug=True)
