import yfinance as yf
import pandas as pd

def get_stock_data(tickers, start, end, interval="1d"):
    # Download all tickers at once, auto-adjusted for splits/dividends
    data = yf.download(
        tickers,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    # 'Close' will now be adjusted prices because auto_adjust=True
    if "Close" in data.columns:
        data = data["Close"]

    # If only one ticker, make sure it's a DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame()

    # Rename columns to just ticker symbols (no multi-index)
    data.columns = [col if isinstance(col, str) else col[1] for col in data.columns]
    return data
