from portfolio_item import PortfolioItem
import streamlit as st
import time
import yfinance as yf
import altair as alt
import pandas as pd
import plotly.express as px
from utils import process_ticker_data, process_stock_data_pipeline


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

    def benchmark_portfolio(self, benchmark_ticker_label="SPY"):
        # Get the benchmarking data
        benchmark_data = process_stock_data_pipeline(benchmark_ticker_label)

        portfolio_data_modified = {key: value for key, value in self.portfolio.items()}

        # Trimming the portfolio timeseries data to have the same periods
        ticker_data_lengths = [
            min(ticker_obj.data["Date"])
            for ticker_obj in portfolio_data_modified.values()
        ]
        start_date = max(ticker_data_lengths)

        for ticker, ticker_obj in portfolio_data_modified.items():
            portfolio_data_modified[ticker].data = ticker_obj.data.loc[
                ticker_obj.data["Date"] >= start_date
            ]

        cum_returns = []
        for ticker_label, ticker_obj in portfolio_data_modified.items():
            # Get all ticker data and create new cumulative returns by using sum product
            # of weights and ticker cumulative returns
            data = ticker_obj.data["CumulReturns"].fillna(0) * float(ticker_obj.weight)

            cum_returns.append(data.values)

        adjusted_cumul_returns = [sum(x) for x in zip(*cum_returns)]

        df = pd.DataFrame(adjusted_cumul_returns)
        df["Symbol"] = "Portfolio"
        df["Date"] = benchmark_data["Date"]

        data_len, bm_len = len(adjusted_cumul_returns), len(benchmark_data)

        if bm_len > data_len:
            start_index = bm_len - data_len
            benchmark_data = benchmark_data.iloc[start_index:, :]
        else:
            start_index = data_len - bm_len
            adjusted_cumul_returns = adjusted_cumul_returns.iloc[start_index:, :]

        # Re-calculate the cumulative returns and normalise both timeseries to have the same starting value, 1

        benchmark_data = process_ticker_data(benchmark_data, normalise=True)

        adjusted_cumul_returns_df = pd.DataFrame(
            adjusted_cumul_returns, columns=["CumulReturns"]
        )

        adjusted_cumul_returns_df["Date"] = benchmark_data["Date"]
        adjusted_cumul_returns_df["Symbol"] = "Portfolio"

        # Normalise the portfolio returns data to start at 1
        adjusted_cumul_returns_df["CumulReturns"] = (
            adjusted_cumul_returns_df["CumulReturns"]
            / adjusted_cumul_returns_df["CumulReturns"].iloc[1]
        ).iloc[
            1:,
        ]

        stock_data = pd.concat([benchmark_data, adjusted_cumul_returns_df])

        fig = px.line(stock_data, x="Date", y="CumulReturns", color="Symbol")

        st.plotly_chart(fig)

    @staticmethod
    def benchmark(ticker_label, benchmark_ticker_label="SPY"):
        """Benchmark the historic returns for the portfolio items against another stock."""

        # Get the benchmarking data
        benchmark_data = process_stock_data_pipeline(benchmark_ticker_label)

        data = process_stock_data_pipeline(ticker_label)

        # Truncate the benchmark data to the same size as the chosen ticker data and
        # recalculate cumulative returns for the same period
        start_date = data["Date"].min()
        data_len, bm_len = len(data), len(benchmark_data)

        if bm_len > data_len:
            start_index = bm_len - data_len
            benchmark_data = benchmark_data.iloc[start_index:, :]
        else:
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
