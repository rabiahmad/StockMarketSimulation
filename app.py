import streamlit as st
import yfinance as yf
import altair as alt
import matplotlib.pyplot as plt
from portfolio_item import PortfolioItem
from portfolio_simulator import PortfolioSimulator

st.title("Stock market simulator")

# User input for tickers
portfolio_tickers = st.text_area(
    label="Enter tickers separated by comma. e.g. AAPL, MSFT",
    value="ISWD.L, HIUS.L, ISUS.L",
)

# User input for chart type. TODO add chart functionality later (low priority)
chart_type = st.selectbox(label="Chart type", options=["Line", "Area", "Candlestick"])


# Split the list of tickers out into a list
portfolio_tickers_list = portfolio_tickers.split(", ")


# Create the portfolio by instantiating PortfolioItems for each ticker whilst fetching required stock market
# data and calculating daily returns using fetch_data method
portfolio = {}
for ticker_label in portfolio_tickers_list:
    ticker = PortfolioItem(ticker_label, 1 / len(portfolio_tickers_list))
    ticker.show()
    ticker.fetch_data()
    portfolio[ticker_label] = ticker


# if chart_type == "Line":
#     line_chart = (
#         alt.Chart(portfolio["ISWD.L"].history)
#         .mark_line()
#         .encode(x="Date:T", y="Close:Q")
#     )
#     line_chart
# elif chart_type == "Area":
#     area_chart = (
#         alt.Chart(portfolio["ISWD.L"].history)
#         .mark_area(
#             line={"color": "darkgreen"},
#             color=alt.Gradient(
#                 gradient="linear",
#                 stops=[
#                     alt.GradientStop(color="white", offset=0),
#                     alt.GradientStop(color="darkgreen", offset=1),
#                 ],
#                 x1=1,
#                 x2=1,
#                 y1=1,
#                 y2=0,
#             ),
#         )
#         .encode(alt.X("Date:T"), alt.Y("Close:Q"))
#     )
#     area_chart
# elif chart_type == "Candlestick":
#     ## Base
#     base = alt.Chart(portfolio["ISWD.L"].history).encode(
#         x=alt.X(
#             "Date:T", axis=alt.Axis(format="%d/%m/%y", labelAngle=-45, title="Date")
#         ),
#         color=alt.condition(
#             "datum.Open <= datum.Close", alt.value("lawngreen"), alt.value("tomato")
#         ),
#     )

#     ## Lines
#     rule = base.mark_rule().encode(
#         y=alt.Y("Low:Q", title="Price", scale=alt.Scale(zero=False)),
#         y2=alt.Y2("High:Q"),
#     )

#     ## Candles
#     bar = (
#         base.mark_bar(width=10.0)
#         .encode(
#             y=alt.Y("Open:Q"),
#             y2=alt.Y2("Close:Q"),
#             tooltip=["Date", "Open", "High", "Low", "Close"],
#         )
#         .properties(width=600, height=300, title="Ticker historic data")
#     )

#     candlestick = rule + bar

#     candlestick


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

simulate_button = st.button(label="Run simulation")

if simulate_button:
    sim.simulate()
