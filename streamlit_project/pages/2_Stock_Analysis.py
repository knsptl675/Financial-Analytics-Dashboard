import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.trend import MACD
st.set_page_config(page_title="Stock Analysis", page_icon="📈", layout="wide")
st.title("📈 Stock Analysis")

# # ---------------- SIDEBAR ----------------

asset = st.sidebar.selectbox(
    "Select Asset",
    ["NVIDIA", "Gold", "Bitcoin"]
)

ticker_map = {
    "NVIDIA": "NVDA",
    "Gold": "GC=F",
    "Bitcoin": "BTC-USD"
}

ticker = ticker_map[asset]

start = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# ---------------- DATA LOADING ----------------
with st.spinner("Downloading market data..."):

    try:
        df = yf.download(ticker, start=start, end=end)
        df.columns = df.columns.get_level_values(0)

        if df.empty:
            st.error("No data found for selected asset.")
            st.stop()

    except:
        st.error("Error downloading data from Yahoo Finance.")
        st.stop()

df = df.reset_index()
df = df.dropna()

close_price = df["Close"].squeeze()

# -------- Daily Change Metric --------

st.subheader("Daily Change")

current_price = df["Close"].iloc[-1]
previous_price = df["Close"].iloc[-2]

daily_change = current_price - previous_price
daily_change_percent = (daily_change / previous_price) * 100

st.metric(
    label="Daily Change",
    value=round(current_price,2),
    delta=f"{round(daily_change,2)} ({round(daily_change_percent,2)}%)"
)

# ---------------- DAILY RETURN ----------------
df["Daily Return"] = close_price.pct_change()

st.subheader("Daily Return")

fig5 = go.Figure()

fig5.add_trace(go.Scatter(x=df["Date"], y=df["Daily Return"], name="Daily Return"))

fig5.update_layout(height=400)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- VOLATILITY ----------------
df["Volatility"] = df["Daily Return"].rolling(20).std()

st.subheader("Volatility (20 Day Rolling)")

fig6 = go.Figure()

fig6.add_trace(go.Scatter(x=df["Date"], y=df["Volatility"], name="Volatility"))

fig6.update_layout(height=400)

st.plotly_chart(fig6, use_container_width=True)

# ---------------- CANDLESTICK ----------------
st.subheader("Candlestick Chart")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df["Date"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"]
))

fig.update_layout(height=600)

st.plotly_chart(fig, use_container_width=True)

# ---------------- MOVING AVERAGE ----------------

df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

st.subheader("Moving Average Analysis")

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df["Date"],
    y=df["Close"],
    mode='lines',
    name="Close Price"
))

fig2.add_trace(go.Scatter(
    x=df["Date"],
    y=df["MA20"],
    mode='lines',
    name="MA20"
))

fig2.add_trace(go.Scatter(
    x=df["Date"],
    y=df["MA50"],
    mode='lines',
    name="MA50"
))

fig2.update_layout(
    height=500,
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis=dict(type="date")
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- RSI ----------------
rsi_indicator = RSIIndicator(close=close_price, window=14)
df["RSI"] = rsi_indicator.rsi()

st.subheader("RSI Indicator")

fig3 = go.Figure()

fig3.add_trace(go.Scatter(x=df["Date"], y=df["RSI"], name="RSI"))

fig3.add_hline(y=70)
fig3.add_hline(y=30)

fig3.update_layout(height=400)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- MACD ----------------
macd_indicator = MACD(close=close_price)

df["MACD"] = macd_indicator.macd()
df["Signal"] = macd_indicator.macd_signal()

st.subheader("MACD Indicator")

fig4 = go.Figure()

fig4.add_trace(go.Scatter(x=df["Date"], y=df["MACD"], name="MACD"))

fig4.add_trace(go.Scatter(x=df["Date"], y=df["Signal"], name="Signal"))

fig4.update_layout(height=400)

st.plotly_chart(fig4, use_container_width=True)

#------- Bollinger Bands --------

# Bollinger Bands Calculation
df["MA20"] = df["Close"].rolling(window=20).mean()
df["STD"] = df["Close"].rolling(window=20).std()

df["Upper_Band"] = df["MA20"] + (df["STD"] * 2)
df["Lower_Band"] = df["MA20"] - (df["STD"] * 2)

st.subheader("Bollinger Bands")

fig = go.Figure()

# Close price
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    name="Close Price"
))

# Middle band
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["MA20"],
    name="Middle Band (MA20)"
))

# Upper band
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Upper_Band"],
    name="Upper Band"
))

# Lower band
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Lower_Band"],
    name="Lower Band"
))

st.plotly_chart(fig, use_container_width=True)

