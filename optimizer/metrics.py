import numpy as np
import pandas as pd

def calculate_risk_metrics(returns: pd.DataFrame, weights: np.ndarray, risk_free_rate: float = 0.0) -> dict:
    
    weights = np.array(weights)
    
    portfolio_returns = returns @ weights

    mean_daily_return = portfolio_returns.mean()
    vol_daily = portfolio_returns.std()

    annual_return = mean_daily_return * 252
    annual_vol = vol_daily * np.sqrt(252)

    # Sharpe Ratio
    sharpe_ratio = (annual_return - risk_free_rate) / annual_vol if annual_vol != 0 else np.nan

    # Sortino Ratio
    downside_returns = portfolio_returns[portfolio_returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(252)
    sortino_ratio = (annual_return - risk_free_rate) / downside_vol if downside_vol != 0 else np.nan

    # Value at Risk (VaR) 95%
    var_95 = np.percentile(portfolio_returns, 5)

    # Conditional VaR (CVaR) 95%
    cvar_95 = portfolio_returns[portfolio_returns <= var_95].mean()

    # Max Drawdown
    cumulative_returns = (1 + portfolio_returns).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdowns = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown = drawdowns.min()

    return {
        "Annual Return": annual_return,
        "Annual Volatility": annual_vol,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "VaR 95%": var_95,
        "CVaR 95%": cvar_95,
        "Max Drawdown": max_drawdown
    }
