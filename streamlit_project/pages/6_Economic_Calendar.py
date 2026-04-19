import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="USD Economic News", page_icon="📅", layout="wide")

st.title("📅 USD Economic News (Live)")
st.write("Latest macroeconomic news affecting Gold and Bitcoin markets")

API_KEY = "096601e0db2c449f827cc061e5826c30"

url = f"https://newsapi.org/v2/everything?q=USD%20economy%20OR%20Federal%20Reserve%20OR%20inflation&language=en&sortBy=publishedAt&apiKey={API_KEY}"

response = requests.get(url)
data = response.json()

articles = data["articles"]

news_list = []

for article in articles[:15]:
    news_list.append({
        "Time": article["publishedAt"],
        "Title": article["title"],
        "Source": article["source"]["name"],
        "Link": article["url"]
    })

df = pd.DataFrame(news_list)

st.subheader("Latest USD Economic News")

st.dataframe(df, use_container_width=True)

st.subheader("Read Full Article")

for article in articles[:5]:
    st.markdown(f"**{article['title']}**")
    st.write(article["description"])
    st.markdown(f"[Read More]({article['url']})")
    st.divider()