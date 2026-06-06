import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analysis")

st.title("📈 AI Stock Analysis Platform")

symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
)

if st.button("Analyze"):

    stock = yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True
    )

    if stock.empty:
        st.error("Invalid Stock Symbol")
    else:
        st.subheader("Latest Data")
        st.dataframe(stock.tail())

        st.subheader("Stock Price Chart")
        st.line_chart(stock["Close"])
