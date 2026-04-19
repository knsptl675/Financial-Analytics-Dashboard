import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("📊 Market Comparison")

st.write("Compare Stock, Commodity and Crypto Markets")

start = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end = st.date_input("End Date", pd.to_datetime("2025-01-01"))

# Download data
nvda = yf.download("NVDA", start=start, end=end)
gold = yf.download("GC=F", start=start, end=end)
btc = yf.download("BTC-USD", start=start, end=end)

# Convert to 1D series
nvda_close = nvda["Close"].squeeze()
gold_close = gold["Close"].squeeze()
btc_close = btc["Close"].squeeze()

# Combine datasets safely
df = pd.concat(
    [nvda_close, gold_close, btc_close],
    axis=1
)

df.columns = ["NVIDIA", "Gold", "Bitcoin"]

st.subheader("Price Comparison")

st.line_chart(df)

# ---------------- RETURNS ----------------

returns = df.pct_change()

st.subheader("Daily Returns")

st.line_chart(returns)

# ---------------- CUMULATIVE RETURN ----------------

cumulative = (1 + returns).cumprod()

st.subheader("Cumulative Returns")

st.line_chart(cumulative)

# ---------------- VOLATILITY ----------------

volatility = returns.std() * 100

st.subheader("Market Volatility (%)")

st.write(volatility)

# ---------------- RISK vs RETURN ----------------

risk = returns.std()
avg_return = returns.mean()

risk_return = pd.DataFrame({
    "Risk": risk,
    "Return": avg_return
})

st.subheader("Risk vs Return")

fig = px.scatter(
    risk_return,
    x="Risk",
    y="Return",
    text=risk_return.index,
    size=[10,10,10],
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- BEST ASSET ----------------

best_asset = cumulative.iloc[-1].idxmax()

st.success(f"Best Performing Asset: {best_asset}")
