import streamlit as st
from portfolio_item import PortfolioItem
from portfolio_simulator import PortfolioSimulator
from utils import portfolio_weight_validator

st.title("Stock market simulator")

# User input for tickers
default_portfolio_string = "HLAL: 0.8, ISUS.L: 0.1, ISWD.L: 0.1"

portfolio_tickers = st.text_area(
    label="Enter portfolio ticker: weights, separated by comma. e.g. AAPL: 0.8, MSFT: 0.2",
    value=default_portfolio_string,
)

# Split the list of tickers out into a list
portfolio_tickers_list = portfolio_tickers.split(", ")


# Create the portfolio by instantiating PortfolioItems for each ticker whilst fetching required stock market
# data and calculating daily returns using fetch_data method
portfolio = {}
for entry in portfolio_tickers_list:
    ticker_label = entry.split(": ")[0]
    weight = entry.split(": ")[1]
    ticker = PortfolioItem(ticker_label, weight)
    # ticker.show()
    ticker.fetch_data()
    portfolio[ticker_label] = ticker


if not portfolio_weight_validator.validate_weights(portfolio):
    st.error("Please ensure portfolio weights add up to 1")

with st.expander(label="Additional inputs #TODO"):
    # User input to define the number of years to forecast
    forecast_years = st.text_input(label="Forecast years", value=5)

    # Investment strategy
    investment_stategy = st.selectbox(
        label="Investment strategy",
        options=[
            "Lump sum one off investment",
            "Yearly investment",
            "Quarterly investment",
            "Monthly investment",
            "Daily investment",
        ],
    )

    investment_amount = st.text_input(label="Investment amount", value=1000)

    reinvest_returns = st.selectbox(label="Re-invest profits", options=["Yes", "No"])

# Simulation methodology:
# 1. Starting point for simulation is X years ago where X is the forecast years
# 2. Using the Daily returns, calculate the cumulative returns for the entire portfolio for the next X years
# (last day would be today) based on the investment strategy selected
# 3. If X years of data is not available for any portfolio item, then cycle through the data in order to
# complete the dataframe


sim = PortfolioSimulator(
    portfolio=portfolio,
    forecast_period=forecast_years,
    investment_strategy=investment_stategy,
    reinvest=reinvest_returns,
    investment_amount=investment_amount,
)


if st.button(label="Run portfolio benchmark"):
    sim.benchmark_portfolio()

if st.button(label="Run individual benchmarks"):
    for ticker in portfolio.keys():
        sim.benchmark(ticker_label=ticker)
