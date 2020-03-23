# from gainers import Gainers
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import math
# import datetime
import gainers
from pprint import pprint
import threading
import json
from functools import reduce
import os
import datetime
import math

error_msg = {
    "max_calls": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.",
    "invalid_call": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_INTRADAY.",
    "timeseries_missing": "Not enought time series data to calculate long_mavg."
}


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


ts = TimeSeries(key='RAVFAINVUAJHR2EW', output_format='pandas')


def getTime(format):
    t = time.localtime(time.time())
    formatTime = time.strftime(format, t)
    return formatTime


class Trader():
    def __init__(self, interval, outputsize, short_window, long_window, budget):
        self.interval = interval
        self.outputsize = outputsize
        self.short_window = short_window
        self.long_window = long_window
        self.budget = float(budget)
        self.money_to_spend = float(budget)
        self.holdings = 0.0
        self.total_money = 0.0
        self.updated_bought_shares = {}
        self.initial_bought_shares = {}
        self.sold_shares = {}
        self.real_gains = 0.0
        self.gains = 0.0

    def createBackup(self):
        t = getTime('%Y-%m-%d')
        print("Local current time :", getTime('%Y-%m-%d %H:%M'))
        createFolder('./backup/')
        with open('./backup/' + t + '.json', "w") as f:
            f.write(json.dumps(self.updated_bought_shares))

    def saveTrades(self, stock_name=None, stock_close=None, t=None, pos=None, num_shares=None):
        num_of_shares = 0.0
        if pos != -1.0:
            if stock_name in self.updated_bought_shares:
                # pos == 0.0
                init_close = float(
                    self.initial_bought_shares[stock_name]['close'])
                initial_close_diff = float(stock_close) - init_close
                init_time = self.initial_bought_shares[stock_name]['time']
                prev_close = float(
                    self.updated_bought_shares[stock_name]['close'])
                prev_close_diff = float(stock_close) - prev_close
                num_of_shares = self.updated_bought_shares[stock_name]['num_shares']
            else:
                # pos == 1.0
                init_close = float(stock_close)
                init_time = str(t)
                initial_close_diff = float(stock_close)
                prev_close = float(stock_close)
                prev_close_diff = 0.0
                num_of_shares = num_shares
                self.holdings += float(stock_close)
                self.money_to_spend -= initial_close_diff
                self.initial_bought_shares[stock_name] = {
                    'close': init_close, 'time': init_time}

            self.holdings += (prev_close_diff * num_of_shares)
            self.total_money = self.holdings + self.money_to_spend
            self.gains = self.total_money - self.budget
            self.real_gains = self.money_to_spend - self.budget
            self.updated_bought_shares[stock_name] = {
                'num_shares': num_of_shares,
                'close': stock_close,
                'close_total': num_of_shares * stock_close,
                'init_close': init_close,
                'initial_close_diff': initial_close_diff,
                'prev_close': prev_close,
                'holdings': self.holdings,
                'total_money': self.total_money,
                'gains': self.gains,
                'real_gains': self.real_gains,
                'money_to_spend': self.money_to_spend,
                'init_time': init_time,
                'time': str(t),

            }
        elif pos == -1.0 and stock_name in self.updated_bought_shares:
            self.money_to_spend += stock_close * num_of_shares
            self.updated_bought_shares.pop(stock_name, None)
            self.initial_bought_shares.pop(stock_name, None)
            self.real_gains = self.money_to_spend - self.budget

    def analyze(self, symbols):
        stock_list = {}
        index = 0
        print(symbols)

        skip_symbols = 0
        while(index < 5):
            symbol = symbols[index + skip_symbols]
            try:
                data, meta_data = ts.get_intraday(
                    symbol=symbol, interval=self.interval, outputsize=self.outputsize)
                
                stock = pd.DataFrame(index=data[::-1].index)
               
                stock['close'] = data['4. close'][::-1]
                stock['short_mavg'] = stock['close'].rolling(
                    window=self.short_window, min_periods=1, center=False).mean()
                stock['long_mavg'] = stock['close'].rolling(
                    window=self.long_window, min_periods=1, center=False).mean()
                if len(stock['long_mavg']) >= self.long_window:
                    stock['signal'] = 0.0       
                    stock['signal'][self.short_window:] = np.where(
                        stock['short_mavg'][self.short_window] > stock['long_mavg'][self.short_window], 1.0, 0.0)
                    # print('Not Working')
                    stock['position'] = stock['signal'].diff()
                    stock_list[symbol] = stock
                    index += 1
                    print('Found: ' + symbol)
                else:
                    raise ValueError('Not enought time series data to calculate long_mavg.')
               
            except Exception as e:
                if str(e) == error_msg['max_calls']:
                    print('Reached call limit, sleeping for 60 seconds ...')
                    time.sleep(60)
                elif str(e) == error_msg['invalid_call']:
                    skip_symbols += 1
                    print('Not found: ' + symbol)
                elif str(e) == error_msg['timeseries_missing']:
                    skip_symbols += 1
                    print('Cannot calculate long_mavg: ' + symbol)
                else:
                    print('Unknown error:', e)
                
        return stock_list

    def trade(self, gainers):
        # gainers = ['AAPL', 'MSFT']
        stocks_to_observe = list(dict.fromkeys(
            list(self.updated_bought_shares.keys()) + gainers))
        stocks = self.analyze(symbols=stocks_to_observe)
        for index, stock_name in enumerate(stocks.keys(), start=0):
            for t, row in stocks[stock_name].iterrows():
                close = float(row['close'])
                position = float(row['position'])

                if stock_name in self.updated_bought_shares:
                    self.saveTrades(stock_name=stock_name,
                                    stock_close=close, t=t)
                    print('Update ' + stock_name, '=>', 'Close=' + str(close),
                          'Gains=' + str(self.gains), "(" + str(t) + ')')

                elif position == 1.0 and stock_name not in self.updated_bought_shares:
                    possible_shares = (self.money_to_spend / 5) / float(close)
                    num_of_shares = math.floor(possible_shares) if possible_shares >= 1.0 else possible_shares
                    self.saveTrades(stock_name=stock_name,
                                    stock_close=close, t=t, num_shares=num_of_shares)
                    print('Buy ' + stock_name, '=>', 'Close=' + str(close), 'Gains=' +
                          str(self.gains), 'Sharenum=' + str(num_of_shares), "(" + str(t) + ')')

                elif position == -1.0 and stock_name in self.updated_bought_shares:
                    self.saveTrades(stock_name=stock_name,
                                    stock_close=close, t=t, pos=position)
                    print('Sell ' + stock_name, '=>', 'Close=' + str(close),
                          'Gains=' + str(self.gains), "(" + str(t) + ')')

        # if self.updated_bought_shares:
        #     pprint(self.updated_bought_shares)
        #     self.saveTrades()

        # some_list = list(self.bought_shares.keys()) + [x for x in gainers if x not in self.bought_shares.keys()]

# # data, meta_data = ti.get_sma(symbol="MSFT", interval='1min', series_type='close', time_period=1440)
# data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')
# # data, meta_data = ts.get_daily(symbol='AAPL', outputsize='compact')

# signals = pd.DataFrame(index=data.index)
# signals['signal'] = 0.0

# signals['short_mavg'] = data['4. close'].rolling(window=short_window, min_periods=1, center=False).mean()

# signals['long_mavg'] = data['4. close'].rolling(window=long_window, min_periods=1, center=False).mean()

# signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window] > signals['long_mavg'][short_window], 1.0, 0.0)

# signals['positions'] = signals['signal'].diff()

# print(signals)

# Plotting

# fig = plt.figure()

# ax1 = fig.add_subplot(111, ylabel='Price in $')

# data['4. close'].plot(ax=ax1, color='r', lw=2.)

# signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# # buy signal
# ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^', markersize=10, color='m')

# # sell signal
# ax1.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v', markersize=10, color='k')

# plt.show()


# gainers = Gainers.now_gainers(5)
# print("Gainers:", gainers)

# def replaceIt(value, sym):
#     for x in sym:
#         value = value.replace(x, '')
#     return value

# def plotIntraday(symbols, interval, outputsize):
#     for symbol in symbols:
#         data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
#         data['4. close'].plot()
#     plt.title('Intraday Times Series for the ' + replaceIt(str(symbols), ['[', ']', "'"]) + ' stocks (' + interval + ')')
#     plt.show()


# plotIntraday([gainers[0]], '60min', 'full')

# ti = TechIndicators(key='RAVFAINVUAJHR2EW', output_format='pandas')
