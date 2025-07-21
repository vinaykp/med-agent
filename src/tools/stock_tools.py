
def get_stock_price(stock_symbol: str) -> float:
    # Placeholder implementation - replace with actual API call or database query
    stock_prices = {
        "AAPL": 150.0,
        "GOOGL": 2800.0,
        "AMZN": 3400.0
    }
    return stock_prices.get(stock_symbol, 0.0)