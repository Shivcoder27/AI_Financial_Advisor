from stock_insights import get_stock_price

def check_risk(symbol):
    price = get_stock_price(symbol)
    if isinstance(price, str):  # Error handling
        return "Unable to fetch stock data."

    # Example threshold conditions
    if price < 100:
        return f"🚨 Warning: {symbol} is trading below $100. High risk!"
    elif price > 500:
        return f"✅ {symbol} is performing well!"
    else:
        return f"⚠️ Monitor {symbol}. Moderate risk."
