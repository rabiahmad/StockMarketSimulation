from utils.process_ticker_data import process_ticker_data
import yfinance as yf


def process_stock_data_pipeline(ticker):
    ticker_obj = yf.Ticker(ticker)
    ticker_data = ticker_obj.history(period="max", interval="1d")
    ticker_data = process_ticker_data(ticker_data)
    ticker_data["Symbol"] = ticker
    return ticker_data
