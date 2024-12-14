import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.header("Indian Stock Dashboard")

# Sidebar inputs
ticker = st.sidebar.text_input("Symbol Code", "INFY")
exchange = st.sidebar.text_input("Exchange", "NSE").upper()

# Generate URL
url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
st.write(f"Fetching data from: {url}")  # Debug output

try:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract data with error handling
        try:
            price = float(soup.find(class_="YMlKec fxKbKc").text.strip()[1:].replace(",", ""))
        except AttributeError:
            price = "N/A"

        try:
            previous_close = float(soup.find(class_="P6K39c").text.strip()[1:].replace(",", ""))
        except AttributeError:
            previous_close = "N/A"

        revenue = soup.find(class_="QXDnM").text if soup.find(class_="QXDnM") else "N/A"
        news = soup.find(class_="yY3Lee").text if soup.find(class_="yY3Lee") else "N/A"
        about = soup.find(class_="bLLb2d").text if soup.find(class_="bLLb2d") else "N/A"

        # Create DataFrame
        data = {
            "Price": price,
            "Previous Close": previous_close,
            "Revenue": revenue,
            "News": news,
            "About": about,
        }
        df = pd.DataFrame(data, index=["Extracted Data"]).T

        # Display Data
        st.write(df)
    else:
        st.error("Failed to fetch data. Please check the stock symbol or try again later.")
except Exception as e:
    st.error(f"An error occurred: {e}")
