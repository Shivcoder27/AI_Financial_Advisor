import requests
import plotly.graph_objects as go
from config import ALPHA_VANTAGE_API_KEY

def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (5min)" in data:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        latest_price = float(data["Time Series (5min)"][latest_time]["1. open"])
        return latest_price
    else:
        return "Error fetching stock price"

def plot_stock_trends(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" in data:
        prices = {date: float(values["4. close"]) for date, values in data["Time Series (Daily)"].items()}
        dates, prices = list(prices.keys()), list(prices.values())

        fig = go.Figure(data=go.Scatter(x=dates, y=prices, mode='lines+markers', name='Stock Price'))
        return fig
    else:
        return None
