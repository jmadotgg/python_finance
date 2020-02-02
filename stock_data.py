# from gainers import Gainers
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas_datareader as pdr 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


import datetime
from pprint import pprint

# dt_unix = datetime.datetime.utcnow().timestamp();
# print('Unix Time:', dt_unix)
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


ts = TimeSeries(key='RAVFAINVUAJHR2EW', output_format='pandas')

class Stocks():
    def __init__(self, symbols, interval, outputsize, short_window, long_window):
       self.symbols = symbols
       self.interval = interval
       self.outputsize = outputsize
       self.short_window = short_window
       self.long_window = long_window
       
    def analyze(self):
        for index, symbol in enumerate(self.symbols, start=0):
            print(symbol, index)
            data, meta_data = ts.get_intraday(symbol=symbol, interval=self.interval, outputsize=self.outputsize)
            signals = pd.DataFrame(index=data.index) if index == 0 else signals
            signals[(symbol + ' short_mavg')] = data['4. close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
            signals[(symbol + ' long_mavg')] = data['4. close'].rolling(window=self.long_window, min_periods=1, center=False).mean()
        return signals
        # signals = pd.DataFrame(index=)

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