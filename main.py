import yfinance as yf

#define the ticker symbol
tickerSymbol = 'VOO'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2000-01-01', end='2021-02-05')

#see your data
print(tickerDf)