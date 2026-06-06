import streamlit as st
import yfinance as yf
import pandas as pd

# Page Config
st.set_page_config(
    page_title="AI Stock Analysis Platform",
    layout="wide"
)

# Title
st.title("📈 AI Stock Analysis Platform")
st.write("Analyze stocks using Technical Indicators")

# Stock Input
symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
)

# Analyze Button
if st.button("Analyze"):

    # Download Stock Data
    stock = yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True
    )

    # Fix Yahoo Finance MultiIndex
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    # Check Data
    if stock.empty:
        st.error("Invalid Stock Symbol")

    else:

        # ------------------------
        # Technical Indicators
        # ------------------------

        # Moving Averages
        stock["MA50"] = stock["Close"].rolling(50).mean()
        stock["MA200"] = stock["Close"].rolling(200).mean()

        # RSI
        delta = stock["Close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        stock["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = stock["Close"].ewm(span=12, adjust=False).mean()
        exp2 = stock["Close"].ewm(span=26, adjust=False).mean()

        stock["MACD"] = exp1 - exp2
        stock["Signal_Line"] = stock["MACD"].ewm(span=9, adjust=False).mean()

        # Latest Values
        current_price = stock["Close"].iloc[-1]
        latest_rsi = stock["RSI"].iloc[-1]
        latest_macd = stock["MACD"].iloc[-1]
        latest_signal = stock["Signal_Line"].iloc[-1]

        # Recommendation Logic
        if latest_rsi < 30 and latest_macd > latest_signal:
            recommendation = "BUY"

        elif latest_rsi > 70 and latest_macd < latest_signal:
            recommendation = "SELL"

        else:
            recommendation = "HOLD"

        # ------------------------
        # Dashboard
        # ------------------------

        st.subheader(f"📊 {symbol} Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Price",
                f"₹{current_price:.2f}"
            )

        with col2:
            st.metric(
                "RSI",
                f"{latest_rsi:.2f}"
            )

        with col3:
            st.metric(
                "MACD",
                f"{latest_macd:.2f}"
            )

        # Recommendation
        st.subheader("Recommendation")

        if recommendation == "BUY":
            st.success("🟢 BUY")

        elif recommendation == "SELL":
            st.error("🔴 SELL")

        else:
            st.warning("🟡 HOLD")

        # Latest Data
        st.subheader("Latest Stock Data")
        st.dataframe(stock.tail())

        # Price + Moving Averages
        st.subheader("Stock Price with MA50 & MA200")

        st.line_chart(
            stock[["Close", "MA50", "MA200"]]
        )

        # RSI Chart
        st.subheader("RSI Chart")

        st.line_chart(
            stock["RSI"]
        )

        # MACD Chart
        st.subheader("MACD Chart")

        st.line_chart(
            stock[["MACD", "Signal_Line"]]
        )

        # Technical Summary
        st.subheader("Technical Analysis Summary")

        summary = pd.DataFrame({
            "Indicator": ["RSI", "MACD", "Signal Line"],
            "Value": [
                round(latest_rsi, 2),
                round(latest_macd, 2),
                round(latest_signal, 2)
            ]
        })

        st.table(summary)

        st.info(
            "This recommendation is based on RSI and MACD indicators only."
        )
