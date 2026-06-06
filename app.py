import streamlit as st

st.title("AI Stock Analysis Platform")

symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")

st.write("Selected Stock:", symbol)
