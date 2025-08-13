# main.py (simplified)
import pandas as pd
from data_fetch.stocks import get_stock_data
from data_fetch.crypto import get_crypto_data
from optimizer.optimize import optimize_portfolio
from visuals.charts import plot_allocation
from optimizer.metrics import calculate_risk_metrics
import matplotlib.pyplot as plt

def main():
    # --- Settings ---
    stocks = ["AAPL", "MSFT", "GOOGL"]
    cryptos = ["BTC-USD", "ETH-USD"]
    start = "2024-01-01"
    end = "2025-08-11"

    # --- Fetch & merge ---
    stock_df = get_stock_data(stocks, start, end)
    crypto_df = get_crypto_data(cryptos, start, end)
    prices = pd.concat([stock_df, crypto_df], axis=1).dropna()

    if prices.empty:
        print("No overlapping data. Try different dates or tickers.")
        return

    # --- Optimize ---
    result = optimize_portfolio(prices)
    weights = result.x
    tickers = prices.columns.tolist()

    # --- Allocation table ---
    weights_df = pd.DataFrame({
        "Ticker": tickers,
        "Allocation (%)": (weights * 100).round(2)
    })
    print("\nOptimal Portfolio Allocation:")
    print(weights_df.to_string(index=False))

     # --- Risk metrics ---
    returns = prices.pct_change().dropna()
    metrics = calculate_risk_metrics(returns, weights)

    print("\nPortfolio Risk Metrics:")
    for k, v in metrics.items():
        if "Ratio" in k:
            print(f"{k}: {v:.3f}")
        else:
            print(f"{k}: {v:.2%}")


    # --- Plot ---
    plot_allocation(weights, tickers)


   
if __name__ == "__main__":
    main()
