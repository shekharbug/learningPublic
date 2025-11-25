import yfinance as yf
from typing import Optional

# To run this script, you must first install the required package:
# pip install yfinance

def get_current_price(ticker_symbol: str) -> Optional[float]:
    """
    Fetches the current market price for a given stock ticker using yfinance.

    This function attempts to retrieve the latest price available for the stock.
    Note: Prices reflect the last close or the latest available market data,
    depending on whether the market is open or closed.

    Args:
        ticker_symbol: The stock ticker symbol (e.g., 'AAPL', 'IRCTC.NS').

    Returns:
        The current price (float) or None if the price could not be retrieved.
    """
    if not ticker_symbol:
        print("Error: Ticker symbol cannot be empty.")
        return None

    try:
        # Create a Ticker object for the specified symbol
        stock = yf.Ticker(ticker_symbol)

        # The 'info' attribute fetches a wealth of data about the company.
        # We look for 'currentPrice' or 'regularMarketPrice'. We use
        # 'currentPrice' as it is often updated in pre/post market sessions too.
        data = stock.info
        
        # Check if the required price data exists in the fetched information
        current_price = data.get('currentPrice')
        
        if current_price is not None:
            return float(current_price)
        else:
            # Fallback to regular market price if currentPrice is not available
            fallback_price = data.get('regularMarketPrice')
            if fallback_price is not None:
                 return float(fallback_price)
            else:
                 print(f"Warning: Price data for {ticker_symbol} not found in the 'info' structure.")
                 return None

    except Exception as e:
        print(f"An error occurred while fetching data for {ticker_symbol}: {e}")
        print("Please check if the ticker symbol is correct and you have an internet connection.")
        return None

# --- Example Usage for IRCTC ---

# The ticker for IRCTC on the National Stock Exchange (NSE) is 'IRCTC.NS'.
IRCTC_TICKER = 'IRCTC.NS'

print(f"Fetching current price for {IRCTC_TICKER}...")
price = get_current_price(IRCTC_TICKER)

if price is not None:
    print(f"\n--- Result ---")
    print(f"Stock: {IRCTC_TICKER}")
    print(f"Current Price: ₹{price:,.2f}")
else:
    print(f"\nFailed to retrieve the price for {IRCTC_TICKER}.")
