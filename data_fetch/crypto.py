import yfinance as yf
import pandas as pd

def get_crypto_data(tickers, start, end, interval="1d"):
    data = yf.download(
        tickers,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if "Close" in data.columns:
        data = data["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame()

    data.columns = [col if isinstance(col, str) else col[1] for col in data.columns]
    return data
