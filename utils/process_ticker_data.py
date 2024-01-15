def process_ticker_data(ticker_data, normalise=False):
    ticker_data = ticker_data.reset_index()
    ticker_data.sort_values("Date")

    ticker_data["PctReturns"] = ticker_data["Close"].pct_change()
    ticker_data["CumulReturns"] = (ticker_data["PctReturns"] + 1).cumprod()

    if normalise:
        ticker_data["CumulReturns"] = (
            ticker_data["CumulReturns"] / ticker_data["CumulReturns"].iloc[1]
        ).iloc[
            1:,
        ]

    return ticker_data
