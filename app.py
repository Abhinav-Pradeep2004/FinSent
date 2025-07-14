# app.py

import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
from src.utils.yfinance_fetcher import fetch_stock_data

# Setup app with SEO metadata
app = dash.Dash(
    __name__,
    title="FinSent – Live Stock Dashboard",
    update_title="Loading FinSent...",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "FinSent is a live stock dashboard with real-time price viewer for AAPL, RELIANCE, TCS, and more."},
        {"name": "keywords", "content": "stock, dashboard, FinSent, yfinance, dash, NSE, BSE, AAPL, RELIANCE"},
        {"name": "author", "content": "Addhyan Nigam"}
    ]
)

server = app.server  # For deployment

# Dropdown options
stock_options = [
    {'label': 'Apple (AAPL)', 'value': 'AAPL'},
    {'label': 'Reliance (RELIANCE.NS)', 'value': 'RELIANCE.NS'},
    {'label': 'Infosys (INFY.NS)', 'value': 'INFY.NS'},
    {'label': 'TCS (TCS.NS)', 'value': 'TCS.NS'},
    {'label': 'Google (GOOG)', 'value': 'GOOG'},
    {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
    {'label': 'Amazon (AMZN)', 'value': 'AMZN'}
]

period_options = ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
interval_options = ["1d", "1h", "30m", "15m", "5m"]

# App layout
app.layout = html.Div(style={'backgroundColor': '#F5F5F5', 'padding': '30px'}, children=[
    html.Div([
        html.H1("📈 FinSent – Stock Price Dashboard",
                style={'textAlign': 'center', 'color': '#1f2937', 'marginBottom': '10px'}),
        html.P("Track real-time stock prices and trends with attractive visuals.", 
               style={'textAlign': 'center', 'color': '#4b5563'}),
    ]),

    html.Div([
        html.Div([
            html.Label("Select Stock", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='ticker-select',
                options=stock_options,
                value='RELIANCE.NS',
                style={'marginBottom': '15px'}
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'paddingRight': '20px'}),

        html.Div([
            html.Label("Select Period", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='period-select',
                options=[{'label': i, 'value': i} for i in period_options],
                value='1mo',
                style={'marginBottom': '15px'}
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select Interval", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='interval-select',
                options=[{'label': i, 'value': i} for i in interval_options],
                value='1d',
                style={'marginBottom': '15px'}
            ),
        ], style={'width': '20%', 'display': 'inline-block', 'paddingLeft': '20px'}),

        html.Div([
            html.Br(),
            html.Button('📥 Fetch Data', id='fetch-btn', n_clicks=0, 
                        style={'backgroundColor': '#2563eb', 'color': 'white', 'padding': '8px 15px',
                               'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'bottom', 'paddingLeft': '30px'})
    ], style={'marginBottom': '30px'}),

    html.Div(id='output-area', style={'marginBottom': '20px', 'fontWeight': 'bold'}),

    html.Div(id='table-container', style={'marginBottom': '30px'}),
    
    html.Div([
        html.H3("📊 Closing Price Trend", style={'color': '#111827'}),
        dcc.Graph(id='line-chart')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'})
])

# Callback
@app.callback(
    [Output('table-container', 'children'),
     Output('line-chart', 'figure'),
     Output('output-area', 'children')],
    [Input('fetch-btn', 'n_clicks')],
    [dash.dependencies.State('ticker-select', 'value'),
     dash.dependencies.State('period-select', 'value'),
     dash.dependencies.State('interval-select', 'value')]
)
def update_stock_data(n_clicks, ticker, period, interval):
    if n_clicks == 0:
        return "", {}, ""

    df = fetch_stock_data(ticker, period, interval)

    if df is None or df.empty:
        return "", {}, html.Div("❌ Error fetching data. Try again.", style={"color": "red"})

    df_reset = df.reset_index()
    table = dash_table.DataTable(
        data=df_reset.tail(10).to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_reset.columns],
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': '#1f2937', 'color': 'white'},
        style_cell={'padding': '8px', 'textAlign': 'left'},
        page_size=10
    )

    figure = {
        'data': [{
            'x': df.index,
            'y': df['Close'],
            'type': 'line',
            'name': ticker,
            'line': {'color': '#2563eb'}
        }],
        'layout': {
            'title': f"Closing Price for {ticker}",
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'},
            'height': 400,
            'plot_bgcolor': 'white'
        }
    }

    return table, figure, html.Div(f"✅ Showing data for {ticker}", style={"color": "green"})

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
