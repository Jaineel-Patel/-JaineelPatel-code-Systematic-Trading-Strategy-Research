import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
           "JPM", "GS", "BAC"] # all the tickers i went to test strategy

data = yf.download(tickers, start="2015-01-01", end="2019-01-01") # download data
data = data["Close"] # only show the Close column

pct_change = ((data - data.shift(20)) / data.shift(20)) * 100 # calculate pct change from day 1 to day 20

signal = (pct_change > 0) * 1 # If 1 that means pct change positive and 0 means negative

returns = ((data-data.shift(1))/data.shift(1)) * 100 # calculate return for each day
strategy_daily_pnl = signal.shift(1) * returns # calculate how much pnl given the signal, avoid look ahead bias
portfolio_pnl = strategy_daily_pnl.mean(axis=1) # Average across 10 tickers for each day
cumulative_pnl = portfolio_pnl.cumsum() #cumulative pnl
print(cumulative_pnl)

benchmark = returns.mean(axis=1).cumsum() #using no strategy
print(benchmark.tail())


plt.plot(cumulative_pnl, label="Strategy")
plt.plot(benchmark, label="Buy & Hold")
plt.legend()
plt.title("Strategy vs Buy & Hold (2015-2019)")
plt.show()

