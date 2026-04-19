import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📄 Stock Information")

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

df = yf.download(ticker, start=start, end=end)

df = df.reset_index()
df = df.dropna()

close_price = df["Close"]

# ---------------- Asset Information ----------------

st.subheader("Asset Information")

if asset == "NVIDIA":
    stock = yf.Ticker("NVDA")

    try:
        info = stock.info
        st.write(info.get("longBusinessSummary", "Information not available"))
    except:
        st.write("Information not available")

elif asset == "Gold":
    
    st.write("""
Gold is a precious metal widely used as a store of value and hedge against inflation. 
It has been used as a form of currency and wealth preservation for thousands of years.

In financial markets, gold is considered a safe-haven asset during economic uncertainty. 
Investors often buy gold when stock markets are volatile or when inflation rises.

Gold prices are influenced by:
• Inflation rates  
• Interest rates  
• US dollar strength  
• Geopolitical tensions  
• Global demand and supply

In trading platforms, gold is commonly traded using the symbol **XAUUSD** or futures ticker **GC=F**.
""")

elif asset == "Bitcoin":

    st.write("""
Bitcoin is the world's first decentralized cryptocurrency created in 2009 by an anonymous person 
or group known as Satoshi Nakamoto.

Unlike traditional currencies, Bitcoin operates on a blockchain network, which records all 
transactions in a secure and transparent way.

Key features of Bitcoin include:
• Decentralized digital currency  
• Limited supply of 21 million coins  
• Global peer-to-peer transactions  
• Highly volatile market price

Bitcoin is widely used for digital payments, trading, and as a speculative investment asset.
In financial markets, it is traded using the ticker **BTC-USD**.
""")
    
# ---------------- Key Metrics ----------------

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", round(close_price.iloc[-1],2))

daily_return = (close_price.iloc[-1] - close_price.iloc[-2]) / close_price.iloc[-2]

col2.metric("Daily Return %", round(daily_return*100,2))

col3.metric("Volume", int(df["Volume"].iloc[-1]))

col4.metric("52W High", round(close_price.max(),2))

# ---------------- Raw Data ----------------

st.subheader("Market Data")

st.dataframe(df.tail(6))