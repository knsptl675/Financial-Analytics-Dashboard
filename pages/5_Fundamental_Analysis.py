import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Fundamental Analysis", page_icon="📊", layout="wide")

st.title("📊 Fundamental Market Analysis")

st.markdown("""
This section analyzes fundamental factors affecting:

• NVIDIA Stock  
• Gold Market  
• Bitcoin Market  
• US Economic Indicators
""")

st.divider()

# NVIDIA FUNDAMENTALS

st.header("NVIDIA Company Fundamentals")

stock = yf.Ticker("NVDA")
info = stock.info

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,.0f}")

with col2:
    st.metric("P/E Ratio", info.get("trailingPE", "N/A"))

with col3:
    st.metric("EPS", info.get("trailingEps", "N/A"))

col4, col5 = st.columns(2)

with col4:
    st.metric("Revenue", f"${info.get('totalRevenue', 0):,.0f}")

with col5:
    st.metric("Profit Margin", info.get("profitMargins", "N/A"))

st.subheader("Company Overview")

st.write(info.get("longBusinessSummary", "No summary available"))

st.divider()

# GOLD FUNDAMENTAL FACTORS

st.header("Gold Market Fundamentals")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
Inflation Impact

Gold prices usually rise when inflation increases because investors use gold as a hedge against inflation.
""")

with col2:
    st.info("""
US Dollar Strength

Gold often moves opposite to the USD. When USD becomes stronger, gold prices may fall.
""")

with col3:
    st.info("""
Geopolitical Risk

Wars or global tensions increase demand for safe-haven assets like gold.
""")

st.divider()

# BITCOIN FUNDAMENTAL FACTORS

st.header("Bitcoin Market Fundamentals")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("""
Institutional Adoption

Large institutions investing in Bitcoin increase market confidence.
""")

with col2:
    st.success("""
Regulation

Government regulations strongly impact cryptocurrency prices.
""")

with col3:
    st.success("""
Supply Limit

Bitcoin has a fixed supply of 21 million coins, making it scarce like gold.
""")

st.divider()

# IMPORTANT ECONOMIC INDICATORS

st.header("Key US Economic Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.warning("""
CPI (Inflation)

Higher inflation often pushes investors towards gold and crypto.
""")

with col2:
    st.warning("""
Interest Rates

Federal Reserve rate decisions move global markets.
""")

with col3:
    st.warning("""
Non-Farm Payrolls

Major employment indicator affecting USD strength.
""")

with col4:
    st.warning("""
GDP Growth

Measures overall economic health.
""")

st.divider()

st.subheader("Market Insight")

st.write("""
Fundamental analysis helps investors understand **why markets move**.

For example:
- High inflation → Gold price rises  
- Institutional demand → Bitcoin rises  
- Strong earnings → NVDA stock increases
""")