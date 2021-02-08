from datetime import datetime
from datetime import date
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def run_simulation(ticker, start_date, freq, amt, output):
    from datetime import datetime
    from datetime import date
    import yfinance as yf
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    import sys
    import warnings

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # get data on this ticker
    tickerData = yf.Ticker(ticker)

    # get the historical prices for this ticker
    cols = ['Open', 'High', 'Low', 'Close']
    tickerDf = tickerData.history(period='1d', start='1975-01-01', end=date.today())[cols]

    df = tickerDf[tickerDf.index >= datetime.strptime(start_date, '%Y-%m-%d')]

    def calculate_contributions(start_date, freq, amt, df):
        df['Date'] = df.index
        df.index = range(len(df))
        df['Contribution'] = 0
        df.loc[(df.index % freq == 0) & (df['Date'] >= datetime.strptime(start_date, '%Y-%m-%d')), 'Contribution'] = amt
        df.index = df['Date']
        df.drop(columns=['Date'], inplace=True)
        df['Cumulative Contributions'] = df['Contribution'].cumsum()

    calculate_contributions(start_date, freq, amt, df)

    # calculating the daily returns
    df['Daily Return'] = df['Close'].pct_change()

    # previous day return
    df['Previous Return'] = df['Close'].pct_change().shift(1)

    tot_bal = []
    for row in range(len(df.index)):
        if str(df.iloc[row]['Previous Return'].item()) == "nan":
            tot_bal.append(df.iloc[row]['Cumulative Contributions'].item())
        else:
            bal = tot_bal[row - 1] * (1 + df.iloc[row - 1]['Daily Return'].item()) + df.iloc[row]['Contribution'].item()
            tot_bal.append(bal)

    TotalBalanceDF = pd.DataFrame({"Total Balance": tot_bal})

    df = pd.concat([df.reset_index(), TotalBalanceDF], axis=1).set_index("Date")

    # calculate the cumulative returns
    df['Cumulative Returns'] = df['Total Balance'] - df['Cumulative Contributions']

    # plot the results
    x = df.index
    y = df[output]
    plt.plot(x, y, label="{}, freq: {}, amt: {} ".format(ticker, freq, amt))
    plt.title("{} {} simulation results".format(ticker, output))
    plt.xlabel("Date")
    plt.ylabel("{}".format(output))
    plt.legend()
    plt.xticks(rotation=45, ha='right')


run_simulation("VOO", "2018-01-01", 365, 2400, "Cumulative Returns")
run_simulation("VOO", "2018-01-01", 30, 200, "Cumulative Returns")
run_simulation("VOO", "2018-01-01", 7, 50, "Cumulative Returns")
plt.rcParams["figure.figsize"] = 30,15