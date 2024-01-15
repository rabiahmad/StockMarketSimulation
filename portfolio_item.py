import streamlit as st
import yfinance as yf
from utils import process_ticker_data


class PortfolioItem(yf.Ticker):
    def __init__(self, ticker_label, weight):
        self.ticker_label = ticker_label
        self.weight = weight

    def fetch_data(self):
        self.ticker = yf.Ticker(self.ticker_label)
        self.data = self.ticker.history(period="max", interval="1d")
        self.data = process_ticker_data(self.data)

    def show(self):
        st.write(f"{self.ticker_label}: {self.weight}")
