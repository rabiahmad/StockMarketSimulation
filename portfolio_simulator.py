from portfolio_item import PortfolioItem
import streamlit as st
import time
import yfinance as yf
import altair as alt
import pandas as pd
import plotly.express as px
from utils import process_ticker_data


class PortfolioSimulator:
    def __init__(
        self,
        portfolio,
        forecast_period,
        investment_strategy,
        reinvest,
        investment_amount,
    ):
        self.portfolio = portfolio
        self.forecast_period = forecast_period
        self.investment_strategy = (investment_strategy,)
        self.reinvest = reinvest
        self.investment_amount = investment_amount

    def simulate(self):
        with st.spinner("Ha. Running simulation"):
            # TODO add actual functionality here
            time.sleep(5)
            st.balloons()

    def benchmark_portfolio(self):
        pass

    @staticmethod
    def benchmark(ticker_label, benchmark_ticker_label="SPY"):
        """Benchmark the historic returns for the portfolio items against another stock."""

        # Get the benchmarking data
        benchmark_ticker = yf.Ticker(benchmark_ticker_label)

        benchmark_data = benchmark_ticker.history(period="max", interval="1d")
        benchmark_data = process_ticker_data(benchmark_data)
        benchmark_data["Symbol"] = benchmark_ticker_label

        st.write(ticker_label)
        ticker = yf.Ticker(ticker_label)
        data = ticker.history(period="max", interval="1d")
        data = process_ticker_data(data)
        data["Symbol"] = ticker_label

        # Truncate the benchmark data to the same size as the chosen ticker data and
        # recalculate cumulative returns for the same period
        start_date = data["Date"].min()
        data_len, bm_len = len(data), len(benchmark_data)
        st.write(data_len)
        st.write(bm_len)

        if bm_len > data_len:
            st.write("#1")
            start_index = bm_len - data_len
            benchmark_data = benchmark_data.iloc[start_index:, :]
        else:
            st.write("#2")
            start_index = data_len - bm_len
            data = data.iloc[start_index:, :]

        # Re-calculate the cumulative returns and normalise both timeseries to have the same starting value, 1
        data = process_ticker_data(data, normalise=True)
        benchmark_data = process_ticker_data(benchmark_data, normalise=True)

        stock_data = pd.concat([benchmark_data, data])

        fig = px.line(stock_data, x="Date", y="CumulReturns", color="Symbol")

        st.markdown(
            f"### {ticker_label} benchmark returns vs S&P500 since {start_date}"
        )
        st.plotly_chart(fig)
