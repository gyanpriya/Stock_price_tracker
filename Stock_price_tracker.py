import requests
import time
from prettytable import PrettyTable

# Alpha Vantage API setup
API_KEY = "SSVR46MMIBVDBT1X"
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol):
    """Fetch real-time stock price from Alpha Vantage API."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Extract the latest stock price
    try:
        last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        stock_price = data["Time Series (1min)"][last_refreshed]["1. open"]
        return float(stock_price)
    except KeyError:
        print("Error: Unable to fetch stock price. Check your API key or symbol.")
        return None

def display_stock_prices(symbols):
    """Display stock prices for given symbols in a table."""
    table = PrettyTable()
    table.field_names = ["Stock Symbol", "Price (USD)"]

    for symbol in symbols:
        price = get_stock_price(symbol)
        if price is not None:
            table.add_row([symbol, f"${price:.2f}"])
        else:
            table.add_row([symbol, "Error"])
    
    print(table)

if __name__ == "__main__":
    # List of stock symbols to track
    stock_symbols = ["AAPL", "GOOGL", "MSFT"]  # Replace with your preferred symbols
    
    print("Real-Time Stock Price Tracker")
    print("-" * 30)

    while True:
        display_stock_prices(stock_symbols)
        print("\nUpdating prices in 60 seconds...\n")
        time.sleep(60)  # Refresh every 60 seconds
