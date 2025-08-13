# app.py
import streamlit as st
import pandas as pd
from datetime import date
from data_fetch.stocks import get_stock_data
from data_fetch.crypto import get_crypto_data
from optimizer.optimize import optimize_portfolio
from visuals.charts import plot_allocation
from optimizer.metrics import calculate_risk_metrics

# Page Config
st.set_page_config(
    page_title="Portfolio Optimizer",
    layout="wide",
    page_icon="logo.jpeg"  # Works with absolute path
)

st.title(" Optimal Portfolio Allocation")

# Logo at top

st.image("logo.jpeg", width=120)

# Yahoo Finance ticker lookup link
st.markdown(
    """
    **Need tickers?**  
    👉 [Yahoo Finance Symbol Lookup](https://finance.yahoo.com/lookup/)  
    Search for stocks, ETFs, and crypto tickers here, then paste them in tickers.
    """
)

# Sidebar inputs
tickers_input = st.sidebar.text_input(
    "Enter tickers (comma-separated)", 
    placeholder="Example: AAPL, GOOGL, MSFT, BTC-USD, ETH-USD"
)
start_date = st.sidebar.date_input("Start Date", date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

if st.sidebar.button("Run Optimization"):
    # Parse tickers
    tokens = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    stock_tickers = [t for t in tokens if "-USD" not in t]
    crypto_tickers = [t for t in tokens if "-USD" in t]

    if not tokens:
        st.error("Please enter at least one ticker.")
        st.stop()

    # Fetch data
    df_list = []
    if stock_tickers:
        df_list.append(get_stock_data(stock_tickers, start=start_date, end=end_date))
    if crypto_tickers:
        df_list.append(get_crypto_data(crypto_tickers, start=start_date, end=end_date))

    prices = pd.concat(df_list, axis=1).dropna()
    if prices.empty:
        st.error("No overlapping data found for the given tickers and date range.")
        st.stop()

    # Optimize portfolio
    result = optimize_portfolio(prices)
    if not getattr(result, "success", True):
        st.error(f"Optimization failed: {result.message}")
        st.stop()

    weights = result.x
    tickers = list(prices.columns)

    # Show allocation chart
    fig = plot_allocation(weights, tickers)
    st.pyplot(fig)

    # Calculate & display risk metrics
    returns = prices.pct_change().dropna()
    metrics = calculate_risk_metrics(returns, weights)

    st.subheader("📈 Portfolio Risk Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Annual Return", f"{metrics['Annual Return']:.2%}")
    col1.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
    col1.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.3f}")
    col2.metric("Sortino Ratio", f"{metrics['Sortino Ratio']:.3f}")
    col2.metric("VaR 95% (daily)", f"{metrics['VaR 95%']:.2%}")
    col2.metric("CVaR 95% (daily)", f"{metrics['CVaR 95%']:.2%}")
    st.write(f"**Max Drawdown:** {metrics['Max Drawdown']:.2%}")

    st.markdown(
    """
    **Disclaimer:**  
    The portfolio optimizer on this site is a tool for 
    demonstration and educational purposes. It uses simplified models 
    and historical data, which may not be representative of future market 
    conditions. The results should not be interpreted as a recommendation or 
    professional financial advice. Please consult with a qualified financial advisor
    before making any investment decisions.
    """
    )

else:
    st.info("💡 Enter tickers and date range in the sidebar, then click **Run Optimization**.")
    st.markdown(
        """"
        **What is a Ticker?**
        A ticker symbol is an abbreviation used to uniquely identify publicly traded 
        companies and other securities on a stock exchange. You can think of it as a 
        company's nickname on the stock market. For instance, AAPL is the ticker for 
        Apple Inc., and MSFT is the ticker for Microsoft. These symbols make it easy 
        for investors to find and trade specific stocks. 
        """
    )
    st.markdown(
    """
    **Disclaimer:**  
    The portfolio optimizer on this site is a tool for 
    demonstration and educational purposes. It uses simplified models 
    and historical data, which may not be representative of future market 
    conditions. The results should not be interpreted as a recommendation or 
    professional financial advice. Please consult with a qualified financial advisor
    before making any investment decisions.
    """
    )

    # Footer Section 
st.markdown("---") 

quote = "“de omnibus dubitandum.” –“Everything must be doubted.” -René Descartes"
contact_email = "finebeard0i@gmail.com"

st.markdown(f"""
<div style='text-align: center; font-size: 16px;'>
    <p><p>
    <p><em>{quote}</em></p>
    <p><p>
    <p>© 2025 Nandyala Sai Chand .</p>
    <p>💬 Mail me to suggest developments or constructive criticism.</p>
    <p>📩 <strong>Contact:</strong> <a href='mailto:{contact_email}'>{contact_email}</a></p>
</div>
""", unsafe_allow_html=True)
