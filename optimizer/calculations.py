import numpy as np
import pandas as pd

def calculate_returns(price_data):
    """Calculate daily returns."""
    return price_data.pct_change().dropna()

def portfolio_performance(weights, mean_returns, cov_matrix):
    """Calculate portfolio return and volatility."""
    returns = np.sum(mean_returns * weights)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, volatility

def sharpe_ratio(returns, volatility, risk_free_rate=0.0):
    """Calculate Sharpe Ratio."""
    return (returns - risk_free_rate) / volatility
