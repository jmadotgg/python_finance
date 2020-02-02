import pandas_datareader as pdr 
import pandas as pd
import datetime

# ! ------------------------------------
# ! IMPORTING FINANCIAL DATA INTO PYTHON
# ! ------------------------------------

aapl = pdr.get_data_yahoo('AAPL', 
start=datetime.datetime(2006, 10, 1),
end=datetime.datetime(2012, 1, 1))

aapl.to_csv('../data/aapl_ohlc.csv')
df = pd.read_csv('../data/aapl_ohlc.csv', header=0, index_col='Date', parse_dates=True)
# print(df)

# Inspect the index 
# aapl.index

# Inspect the columns
# aapl.columns

# Select only the last 10 observations of `Close`
# ts = aapl['Close'][-10:]

# Check the type of `ts` 
# type(ts)

# ! ==================

# Inspect the first rows of November-December 2006
# print(aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].loc())

# Inspect the first rows of 2007 
# print(aapl.loc['2007'].head())

# Inspect November 2006
# print(aapl.iloc[0:1])

# Inspect the 'Open' and 'Close' values at 2006-11-01 and 2006-12-01
# print(aapl.iloc[[22,43], [0, 3]])

# ! ==================

# Sample 20 rows 
# TODO Random sample from data
# sample = aapl.sample(2) 

# Print `sample`
# print(sample)

# Resample to monthly level 
# TODO Only show one (last) day in month for every month
# monthly_aapl = aapl.resample('M').mean()

# Print `monthly_aapl`
# print(monthly_aapl)

# ! ==================

# Add a column `diff` to `aapl` 
# TODO Show difference between opening and closing and save it as a new column in aapl
# aapl['diff'] = aapl.Open - aapl.Close
# print(aapl)
# Delete the new `diff` column
# del aapl['diff']


# ! ----------------------------
# ! VISUALIZING TIME SERIES DATA
# ! ----------------------------

# Import Matplotlib's `pyplot` module as `plt`
# import matplotlib.pyplot as plt

# Plot the closing prices for `aapl`
# aapl['Close'].plot(grid=True)

# Show the plot
# plt.show()

# ! ==================

# TODO Calculating percentage changes for each day
# Import `numpy` as `np`
import numpy as np

# Assign `Adj Close` to `daily_close`
daily_close = aapl[['Adj Close']]

# Daily returns
# daily_pct_change = daily_close.pct_change()

# Replace NA values with 0
# daily_pct_change.fillna(0, inplace=True)

# Inspect daily returns
# print(daily_pct_change)

# Daily log returns (lograrithm)
# daily_log_returns = np.log(daily_close.pct_change()+1)

# Print daily log returns
# print(daily_log_returns)

# ! ==================

# TODO Resample data to get developement from month to month or quarter to quarter
# Resample `aapl` to business months, take last observation as value 
# monthly = aapl.resample('BM').apply(lambda x: x[-1])
# print(monthly)

# Calculate the monthly percentage change
# monthly.pct_change()

# Resample `aapl` to quarters, take the mean as value per quarter
# quarter = aapl.resample("4M").mean()
# print(quarter)

# Calculate the quarterly percentage change
# quarter.pct_change()

# ! ==================

# TODO Different way to calculate percentage changes
# Daily returns
daily_pct_change = daily_close / daily_close.shift(1) - 1

# Print `daily_pct_change`
# print(daily_pct_change)
# print(daily_close)
# print(daily_close / daily_close.shift(1))

# ! ==================

# Import matplotlib
import matplotlib.pyplot as plt

# TODO Show the spread of changes over time
# Plot the distribution of `daily_pct_c`
# daily_pct_change.hist(bins=50)

# Show the plot
# plt.show()

# TODO Show general statistics like max, min and average (mean)
# Pull up summary statistics
# TODO 25% = 25% of percentiles fall below that value (50% and 75% follow the same principle)
# print(daily_pct_change.describe())

# ! ==================

# TODO Show overall return at regular intervals --> determines value of an investment
# Calculate the cumulative daily returns
cum_daily_return = (1 + daily_pct_change).cumprod()

# Plot teh cumulative daily returns
# cum_daily_return.plot(figsize=(12, 8))
# plt.show()

# Print `cum_daily_return`
# print(cum_daily_return)

# Calculate the cumulative monthly return by resampling daily return
# cum_monthly_return = cum_daily_return.resample("M").mean()

# Print cumulative monnthly return
# print(cum_monthly_return)


# ! ----------------------------------
# ! LOAD MORE DATA FROM YAHOO! FINANCE
# ! ----------------------------------

# TODO Tickers = companies history
# Load in data form Apple, Microsoft, IBM and Google from Yahoo! Finance
def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map (data, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2012, 1, 1))

# print(all_data)

# Plot data
# TODO Remove unnecessary columns for plotting
# Isolate the `Adj Close` values and transform the DataFrame
# daily_close_px = all_data[['Adj Close']].reset_index().pivot('Date', 'Ticker', 'Adj Close')

# Calculate the daily percentage for `daily_close_px`
# daily_pct_change = daily_close_px.pct_change()

# Plot the distributions 
# daily_pct_change.hist(bins=50, sharex=True, figsize=(12, 8))

# Show the resulting plot
# plt.show()

# Plot a scatter matrix with the `daily_pct_change` data
# TODO KDE = Kernel Density Estimate (KDE) plot
# pd.plotting.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1, figsize=(12, 12))

# Show the plot
# plt.show()


# ! ----------------------------------
# ! MOVING WINDOWS
# ! ----------------------------------

# TODO Meaning depends on statistic that you apply to the data
# TODO For example a rolling mean smoothes out short-term fluctuations and highlight longer-term trends in data

# Isolate the adjusted closing prices
adj_close_px = aapl['Adj Close']

# Calculate the moving average
# moving_avg = adj_close_px.rolling(window=40).mean()

# Inspect the resulting
# print(moving_avg[-10:])

# Short moving window rolling mean
# aapl['42'] = adj_close_px.rolling(window=40).mean()

# Long moving window rolling mean
# aapl['252'] = adj_close_px.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means 
# aapl[['Adj Close', '42', '252']].plot()

# Show plot
# plt.show()


# ! ----------------------------------
# ! VOLATILITY CALCULATION 
# ! ----------------------------------

# TODO Means measurement of change in variance in the returns of a stock over a specific period of time (smaller is better)

# Define the minimum of periods to consider 
# min_periods = 75 

# Calculate the volatility
# vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

# Plot the volatility
# vol.plot(figsize=(10, 8))

# Show the plot
# plt.show()

# ! ---------------------------------------
# ! ORDINARY LEAST-SQUARES REGRESSION (OLS) 
# ! ---------------------------------------

# TODO Regression analysis

# Import the ´api´ model of ´statsmodels´ under alias ´sm´
import statsmodels.api as sm

# Import the ´datetools´ module from ´pandas´
# import pandas.core.tools.datetimes as datetools

# Isolate the adjusted closing price
all_adj_close = all_data[['Adj Close']]

# Calculate the returns
all_returns = np.log(all_adj_close / all_adj_close.shift(1))

# Isolate the AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')

# Isolate the MSFT returns
msft_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker')

# Build up a new DataFrame with AAPL adn MSFT returns
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']

# Add a constant 
X = sm.add_constant(return_data['AAPL'])

# Construct the model
model = sm.OLS(return_data['MSFT'], X).fit()

# Print the summary
# print(model.summary())

# ! --- Plotting ---

# Plot returns of AAPL and MSFT
# plt.plot(return_data['AAPL'], return_data['MSFT'], 'r.')

# Add an axis to the plot
# ax = plt.axis()

# Initialize `x`
# x = np.linspace(ax[0], ax[1] + 0.01)

# Plot the regression line
# plt.plot(x, model.params[0] + model.params[1] * x, 'b', lw=2)

# Customize the plot
# plt.grid(True)
# plt.axis('tight')
# plt.xlabel('Apple Returns')
# plt.ylabel('Microsoft returns')

# Show the plot
# plt.show()

# TODO Check results from above
# Plot the rolling correlation
# return_data['MSFT'].rolling(window=252).corr(return_data['AAPL']).plot()

# Show the plot
# plt.show()


# ! ---------------------------------------
# ! BUILDING A TRADING STRATEGY WITH PYTHON 
# ! ---------------------------------------

# TODO Start with SIMPLE MOVING AVERAGE (SMA)

# Initialize the short and long moving windows 
short_window = 40
long_window = 100

# Initatialize the ´signals´ DataFrame with the ´signal´ column 
signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

# Create short moving average over the short window
signals['short_mavg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long moving average over the long window
signals['long_mavg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

# Generate trading orders
signals['positions'] = signals['signal'].diff()

# Print ´signals´
# print(signals)

# ! --- Plotting ---

# Iniatialize the  plot figure
# fig = plt.figure()

# Add a subplot and labe for y-axis
# ax1 = fig.add_subplot(111, ylabel='Price in $')

# Plot the closing price
# aapl['Close'].plot(ax=ax1, color='r', lw=2.)

# Plot the short and long moving averages
# signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
# ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^', markersize=10, color='m')

# Plot the buy signals
# ax1.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v', markersize=10, color='k')


# Show the plot
# plt.show()

# TODO Backtesting --> See if trading strategy performs well enough

# Set the initial capital
initial_capital= float(100.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions['AAPL'] = 10*signals['signal']   
  
# Initialize the portfolio with value owned   
portfolio = positions.multiply(aapl['Adj Close'], axis=0)

# Store the difference in shares owned 
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(aapl['Adj Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initial_capital - (pos_diff.multiply(aapl['Adj Close'], axis=0)).sum(axis=1).cumsum()   

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Print the first lines of `portfolio`
# print(portfolio.head())

# ! Visualize portfolio value over years (portfolio['total'])

# Create a figure
# fig = plt.figure()

# ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

# Plot the equity curve in dollars
# portfolio['total'].plot(ax=ax1, lw=2.)

# ax1.plot(portfolio.loc[signals.positions == 1.0].index, 
#          portfolio.total[signals.positions == 1.0],
#          '^', markersize=10, color='m')
# ax1.plot(portfolio.loc[signals.positions == -1.0].index, 
#          portfolio.total[signals.positions == -1.0],
#          'v', markersize=10, color='k')

# Show the plot
# plt.show()

# TODO See Quantopian for backtesting

# ! Evaluating Moving Average Crossover Strategy

# TODO Ratio between returns and risk
# Isolate the returns of your strategy
# returns = portfolio['returns']

# annualized Sharpe ratio
# sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

# Print the Sharpe ratio
# print(sharpe_ratio)

# ! Maximum Drawdown
# TODO Largest single drop from peak to bottom in portfolio, determines risk of portfolio based on strategy

# Define a trailing 252 trading day window
# window = 252

# Calculate the max drawdown in the past window days for each day 
# rolling_max = aapl['Adj Close'].rolling(window, min_periods=1).max()
# daily_drawdown = aapl['Adj Close']/rolling_max - 1.0

# Calculate the minimum (negative) daily drawdown
# max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

# Plot the results
# daily_drawdown.plot()
# max_daily_drawdown.plot()

# Show the plot
# plt.show()

# ! Compound Annual Growth Rate (CAGR)
# TODO Provides constant rate of return over the time period = (investment_ending/investment_begin)^1/n=periods - 1

# Get the number of days in `aapl`
days = (aapl.index[-1] - aapl.index[0]).days

# Calculate the CAGR 
cagr = ((((aapl['Adj Close'][-1]) / aapl['Adj Close'][1])) ** (365.0/days)) - 1

# Print the CAGR
print(cagr)