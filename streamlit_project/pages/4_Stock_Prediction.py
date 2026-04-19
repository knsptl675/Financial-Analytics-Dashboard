import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

st.title("🔮 Market Price Prediction (SARIMA)")

# Asset selection
asset = st.selectbox(
    "Select Asset",
    ["NVIDIA", "Gold", "Bitcoin"]
)

ticker_map = {
    "NVIDIA": "NVDA",
    "Gold": "GC=F",
    "Bitcoin": "BTC-USD"
}

ticker = ticker_map[asset]

# Download historical data
df = yf.download(ticker, start="2020-01-01")

close = df["Close"]

# Select historical range
history_days = st.slider(
    "Historical Days to Display",
    30,
    365,
    90
)

# Forecast range
forecast_days = st.slider(
    "Forecast Days",
    10,
    180,
    90
)

# Train SARIMA
model = SARIMAX(
    close,
    order=(1,1,1),
    seasonal_order=(1,1,1,12)
)

model_fit = model.fit()

# Forecast
forecast_result = model_fit.get_forecast(steps=forecast_days)

forecast = forecast_result.predicted_mean
conf_int = forecast_result.conf_int()

# Create future dates
last_date = close.index[-1]

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=forecast_days
)

forecast.index = future_dates
conf_int.index = future_dates

# Last N historical days
recent_history = close.tail(history_days)

# Plot
fig, ax = plt.subplots(figsize=(12,6))

# Historical
ax.plot(
    recent_history,
    label="Historical Price"
)

# Forecast
ax.plot(
    forecast,
    linestyle="dashed",
    color="red",
    label="Forecast"
)

# Confidence interval
ax.fill_between(
    future_dates,
    conf_int.iloc[:,0],
    conf_int.iloc[:,1],
    alpha=0.3,
    label="Confidence Interval"
)

# Today line
ax.axvline(
    x=last_date,
    linestyle="--",
    label="Today Close"
)

ax.set_title(f"{asset} Price Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Price")

ax.legend()

st.pyplot(fig)

# Forecast table
st.subheader("Forecast Data")

forecast_df = pd.DataFrame({
    "Forecast Price": forecast,
    "Lower Bound": conf_int.iloc[:,0],
    "Upper Bound": conf_int.iloc[:,1]
})

st.dataframe(forecast_df)