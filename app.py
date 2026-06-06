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

    # Fix MultiIndex columns
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    if stock.empty:
        st.error("Invalid Stock Symbol")

    else:
        st.subheader("Latest Data")
        st.dataframe(stock.tail())

        # ADD THE TECHNICAL INDICATOR CODE HERE

            stock["MA50"] = stock["Close"].rolling(50).mean()
    stock["MA200"] = stock["Close"].rolling(200).mean()

        delta = stock["Close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        stock["RSI"] = 100 - (100 / (1 + rs))

        exp1 = stock["Close"].ewm(span=12, adjust=False).mean()
        exp2 = stock["Close"].ewm(span=26, adjust=False).mean()

        stock["MACD"] = exp1 - exp2
        stock["Signal_Line"] = stock["MACD"].ewm(span=9, adjust=False).mean()

        latest_rsi = stock["RSI"].iloc[-1]
        latest_macd = stock["MACD"].iloc[-1]
        latest_signal = stock["Signal_Line"].iloc[-1]

        if latest_rsi < 30 and latest_macd > latest_signal:
            recommendation = "BUY"
        elif latest_rsi > 70 and latest_macd < latest_signal:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"

        st.subheader("Technical Analysis")

        st.write("RSI:", round(latest_rsi, 2))
        st.write("MACD:", round(latest_macd, 2))
        st.write("Signal Line:", round(latest_signal, 2))

        st.success(f"Recommendation: {recommendation}")

        # EXISTING CHART CODE BELOW

        st.subheader("Stock Price Chart")
        st.line_chart(stock[["Close"]])
