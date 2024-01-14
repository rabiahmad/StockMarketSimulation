import streamlit as st
import yfinance as yf


class PortfolioItem(yf.Ticker):
    def __init__(self, ticker_label, weight):
        self.ticker_label = ticker_label
        self.weight = weight
        self.ticker = yf.Ticker(self.ticker_label)

    def fetch_data(self):
        self.data = self.ticker.history(period="max", interval="1d").reset_index()
        self.data["PctReturns"] = self.data["Close"].pct_change()

    def show(self):
        st.write(f"{self.ticker_label}: {self.weight}")
