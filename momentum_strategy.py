import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
           "JPM", "GS", "BAC"] # all the tickers i went to test strategy

data = yf.download(tickers, start="2015-01-01", end="2019-01-01") # download data
data = data["Close"] # only show the Close column

def backtest(data, signal):

    returns = ((data-data.shift(1))/data.shift(1)) * 100 # calculate return for each day
    strategy_daily_pnl = signal.shift(1) * returns # calculate how much pnl given the signal, avoid look ahead bias
    portfolio_pnl = strategy_daily_pnl.mean(axis=1) # Average across 10 tickers for each day
    cumulative_pnl = portfolio_pnl.cumsum() #cumulative pnl

    Sharpe_Ratio = (portfolio_pnl.mean()/portfolio_pnl.std()) * np.sqrt(252) # Calculating Sharpe Ratio which is return over risk
    benchmark = returns.mean(axis=1).cumsum() #using no strategy

    return benchmark, cumulative_pnl, Sharpe_Ratio


pct_change = ((data - data.shift(20)) / data.shift(20)) * 100 # calculate pct change from day 1 to day 20
signal = (pct_change > 0).astype(int)  # If 1 that means pct change positive and 0 means negative
benchmark, cumulative_pnl, Sharpe_Ratio = backtest(data, signal)

mean_rev_signal = (pct_change < 0).astype(int) # mean reversion is the opposite since want to buy when low and sell when high
benchmark, cumulative_pnl_mr, Sharpe_Ratio_mr = backtest(data, mean_rev_signal) 

#Printing the Sharpe Ration respective to each one, and PNL for each one 
print("Mean Reversion Sharpe Ratio:", Sharpe_Ratio_mr)
print("Momentum Sharpe Ratio:", Sharpe_Ratio)
print("PNL FOR MOMENTUM STRATEGY: " ,cumulative_pnl.tail())
print("PNL FOR MEAN REVERSION STRATEGY: ", cumulative_pnl_mr.tail())
print("PNL FOR BENCHMARK (HOLD): ", benchmark.tail())

#PLOTTING THE GRAPH
plt.plot(cumulative_pnl, label="Strategy")
plt.plot(cumulative_pnl_mr, label="Mean Reversion")
plt.plot(benchmark, label="Buy & Hold")
plt.legend()
plt.title("Strategy vs Buy & Hold (2015-2019)")
plt.show()
