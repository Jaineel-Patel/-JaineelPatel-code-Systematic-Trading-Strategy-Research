import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
           "JPM", "GS", "BAC"] # all the tickers i went to test strategy

data = yf.download(tickers, start="2015-01-01", end="2019-01-01") # download data
data = data["Close"] # only show the Close column

# Calculation for momentum and mean reversion strat
def backtest(data, signal):

    returns = ((data-data.shift(1))/data.shift(1)) * 100 # calculate return for each day
    strategy_daily_pnl = signal.shift(1) * returns # calculate how much pnl given the signal, avoid look ahead bias
    portfolio_pnl = strategy_daily_pnl.mean(axis=1) # Average across 10 tickers for each day
    cumulative_pnl = portfolio_pnl.cumsum() #cumulative pnl

    Sharpe_Ratio = (portfolio_pnl.mean()/portfolio_pnl.std()) * np.sqrt(252) # Calculating Sharpe Ratio which is return over risk
    benchmark = returns.mean(axis=1).cumsum() #using no strategy
    rolling_max = cumulative_pnl.cummax()
    maximum_drawdown = (rolling_max - cumulative_pnl).max()


    return benchmark, cumulative_pnl, Sharpe_Ratio, maximum_drawdown


pct_change = ((data - data.shift(20)) / data.shift(20)) * 100 # calculate pct change from day 1 to day 20
signal = (pct_change > 0).astype(int)  # If 1 that means pct change positive and 0 means negative
benchmark, cumulative_pnl, Sharpe_Ratio, maximum_drawdown  = backtest(data, signal)

mean_rev_signal = (pct_change < 0).astype(int) # opposite since buy low sell high
benchmark, cumulative_pnl_mr, Sharpe_Ratio_mr , maximum_drawdown_mr = backtest(data, mean_rev_signal) 


#Displaying information

print(f"{'Strategy':<20} {'Cumulative Return':<20} {'Sharpe':<10} {'Max Drawdown':<15}")
print(f"{'Momentum':<20} {cumulative_pnl.iloc[-1]:<20.2f} {Sharpe_Ratio:<10.2f} {maximum_drawdown:<15.2f}")
print(f"{'Mean Reversion':<20} {cumulative_pnl_mr.iloc[-1]:<20.2f} {Sharpe_Ratio_mr:<10.2f} {maximum_drawdown_mr:<15.2f}")
print(f"{'Buy and Hold':<20} {benchmark.iloc[-1]:<20.2f} {'-':<10} {'-':<15}")

#PLOTTING THE GRAPH
plt.plot(cumulative_pnl, label="Strategy")
plt.plot(cumulative_pnl_mr, label="Mean Reversion")
plt.plot(benchmark, label="Buy & Hold")
plt.legend()
plt.title("Strategy vs Buy & Hold (2015-2019)")
plt.show()
