import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
           "JPM", "GS", "BAC"] # all the tickers i went to test strategy

data = yf.download(tickers, start="2015-01-01", end="2020-01-01") # download data
data = data["Close"] # only show the Close column

test_data = yf.download(tickers, start="2020-01-01", end="2023-01-01") # download data
test_data = test_data["Close"] # only show the Close column

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
    win_rate = ((portfolio_pnl>0).sum()/ len(portfolio_pnl)) * 100



    return benchmark, cumulative_pnl, Sharpe_Ratio, maximum_drawdown, win_rate




pct_change = ((data - data.shift(20)) / data.shift(20)) * 100 # calculate pct change from day 1 to day 20
signal = (pct_change > 0).astype(int)  # If 1 that means pct change positive and 0 means negative
benchmark, cumulative_pnl, Sharpe_Ratio, maximum_drawdown,win_rate  = backtest(data, signal)

#signal for buy and hold
buy_hold_signal = pd.DataFrame(1, index=data.index, columns=data.columns)

benchmark, cumulative_pnl_bh, Sharpe_Ratio_bh, maximum_drawdown_bh, win_rate_bh = backtest(data, buy_hold_signal)

#signal for mean reversion
mean_rev_signal = (pct_change < 0).astype(int) # opposite since buy low sell high
benchmark, cumulative_pnl_mr, Sharpe_Ratio_mr , maximum_drawdown_mr, win_rate_mr = backtest(data, mean_rev_signal)


#signal for volatility_breakout
rolling_high = data.rolling(20).max() # Max price for last 20 days
vb_signal = (data == rolling_high).astype(int) # 1 for whenever the price is equal to max price
benchmark, cumulative_pnl_vb, Sharpe_Ratio_vb, maximum_drawdown_vb, win_rate_vb = backtest(data,vb_signal)



#Displaying information

print("IN SAMPLE 2015-2019")
print(f"{'Strategy':<20} {'Cumulative Return':<20} {'Sharpe':<10} {'Max Drawdown':<15} {'Win Rate':<10}")
print(f"{'Momentum':<20} {cumulative_pnl.iloc[-1]:<20.2f} {Sharpe_Ratio:<10.2f} {maximum_drawdown:<15.2f} {win_rate:<10.2f}")
print(f"{'Mean Reversion':<20} {cumulative_pnl_mr.iloc[-1]:<20.2f} {Sharpe_Ratio_mr:<10.2f} {maximum_drawdown_mr:<15.2f} {win_rate_mr:<10.2f}")
print(f"{'Volatility Breakout':<20} {cumulative_pnl_vb.iloc[-1]:<20.2f} {Sharpe_Ratio_vb:<10.2f} {maximum_drawdown_vb:<15.2f} {win_rate_vb:<10.2f}")
print(f"{'Buy and Hold':<20} {cumulative_pnl_bh.iloc[-1]:<20.2f} {Sharpe_Ratio_bh:<10.2f} {maximum_drawdown_bh:<15.2f} {win_rate_bh:<10.2f}")

#PLOTTING THE GRAPH
plt.figure()
plt.plot(cumulative_pnl, label="Momentum ")
plt.plot(cumulative_pnl_mr, label="Mean Reversion")
plt.plot(cumulative_pnl_vb, label = "Volatility Breakout")
plt.plot(cumulative_pnl_bh, label="Buy & Hold")
plt.legend()
plt.title("Strategy vs Buy & Hold (2015-2019)")
plt.show()


pct_change = ((test_data - test_data.shift(20)) / test_data.shift(20)) * 100 # calculate pct change from day 1 to day 20
signal = (pct_change > 0).astype(int)  # If 1 that means pct change positive and 0 means negative
benchmark, cumulative_pnl, Sharpe_Ratio, maximum_drawdown,win_rate  = backtest(test_data, signal)

#signal for buy and hold
buy_hold_signal = pd.DataFrame(1, index=test_data.index, columns=test_data.columns)

benchmark, cumulative_pnl_bh, Sharpe_Ratio_bh, maximum_drawdown_bh, win_rate_bh = backtest(test_data, buy_hold_signal)

#signal for mean reversion
mean_rev_signal = (pct_change < 0).astype(int) # opposite since buy low sell high
benchmark, cumulative_pnl_mr, Sharpe_Ratio_mr , maximum_drawdown_mr, win_rate_mr = backtest(test_data, mean_rev_signal)


#signal for volatility_breakout
rolling_high = test_data.rolling(20).max() # Max price for last 20 days
vb_signal = (test_data == rolling_high).astype(int) # 1 for whenever the price is equal to max price
benchmark, cumulative_pnl_vb, Sharpe_Ratio_vb, maximum_drawdown_vb, win_rate_vb = backtest(test_data,vb_signal)



#Displaying information

print("OUT OF SAMPLE 2020-2022")
print(f"{'Strategy':<20} {'Cumulative Return':<20} {'Sharpe':<10} {'Max Drawdown':<15} {'Win Rate':<10}")
print(f"{'Momentum':<20} {cumulative_pnl.iloc[-1]:<20.2f} {Sharpe_Ratio:<10.2f} {maximum_drawdown:<15.2f} {win_rate:<10.2f}")
print(f"{'Mean Reversion':<20} {cumulative_pnl_mr.iloc[-1]:<20.2f} {Sharpe_Ratio_mr:<10.2f} {maximum_drawdown_mr:<15.2f} {win_rate_mr:<10.2f}")
print(f"{'Volatility Breakout':<20} {cumulative_pnl_vb.iloc[-1]:<20.2f} {Sharpe_Ratio_vb:<10.2f} {maximum_drawdown_vb:<15.2f} {win_rate_vb:<10.2f}")
print(f"{'Buy and Hold':<20} {cumulative_pnl_bh.iloc[-1]:<20.2f} {Sharpe_Ratio_bh:<10.2f} {maximum_drawdown_bh:<15.2f} {win_rate_bh:<10.2f}")

#PLOTTING THE GRAPH
plt.figure()
plt.plot(cumulative_pnl, label="Momentum ")
plt.plot(cumulative_pnl_mr, label="Mean Reversion")
plt.plot(cumulative_pnl_vb, label = "Volatility Breakout")
plt.plot(cumulative_pnl_bh, label="Buy & Hold")
plt.legend()
plt.title("Strategy vs Buy & Hold (2020-2022)")
plt.show()
