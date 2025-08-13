# optimizer/optimize.py

import numpy as np
from scipy.optimize import minimize

def neg_sharpe(weights, mean_returns, cov_matrix, risk_free_rate=0.0):
    """Negative Sharpe Ratio (to minimize)."""
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return -sharpe_ratio  # negative for minimization

def optimize_portfolio(prices, risk_free_rate=0.0):
    # Calculate daily returns, mean returns, and covariance matrix
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)

    # Constraints: weights sum to 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # Bounds: weights between 0 and 1
    bounds = tuple((0, 1) for _ in range(num_assets))

    # Initial guess: equal allocation
    initial_guess = num_assets * [1. / num_assets]

    # Run optimization
    result = minimize(
        neg_sharpe,
        x0=initial_guess,
        args=args,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        print(f"⚠ Optimization failed: {result.message}")
    else:
        print("✅ Optimization succeeded.")

    return result
