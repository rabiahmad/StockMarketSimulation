from portfolio_item import PortfolioItem
import streamlit as st
import time


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
