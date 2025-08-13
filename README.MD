# Portfolio Risk Optimizer 

1. Pulls daily closing prices for any combination of **stocks** and **cryptocurrencies**.
2. Runs a **mean-variance optimization** to find the portfolio weights that maximize the **Sharpe ratio**.
3. Computes key **risk metrics** (Sharpe, Sortino, VaR, CVaR, Max Drawdown).
4. Visualizes the optimal allocation with an **interactive pie chart**.



**Data**: `yfinance`
**Optimization**: `scipy.optimize`
**Metrics**: Numpy / Pandas
**Visualization**: `matplotlib`


Disclaimer:
This portfolio optimizer  is a tool for demonstration and educational purposes. It uses simplified models and historical data, which may not be representative of future market conditions. The results should not be interpreted as a recommendation or professional financial advice. Please consult with a qualified financial advisor before making any investment decisions.


## 📦 Installation
```bash
pip install -r requirements.txt
streamlit run app.py
