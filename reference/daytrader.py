# Documentation: https://github.com/RomelTorres/alpha_vantage

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import math
import matplotlib.pyplot as plt
from pprint import pprint

# ! Time Series

ts = TimeSeries(key='RAVFAINVUAJHR2EW', output_format='pandas')

# Get json object with the intraday data and another wiht the call's metadata
# data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')
# data['4. close'].plot()

# pprint(data.head(1000))
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show() 




# ! Technical indicators

# ti = TechIndicators(key='RAVFAINVUAJHR2EW', output_format='pandas')

# data, meta_data = ti.get_bbands(symbol="MINE", interval='60min', time_period=60)
# data.plot()

# pprint(data.head())
# plt.title('BBbands indicator for MSFT stock (60 min)')
# plt.show()


# ! Sector performance

# sp = SectorPerformances(key='RAVFAINVUAJHR2EW', output_format='pandas')

# data, meta_data = sp.get_sector()
# data['Rank A: Real-Time Performance'].plot(kind='bar')

# plt.title('Real Time Performance (%) per Sector')
# plt.tight_layout()
# plt.grid()
# plt.show()


# ! Crypto currencies

# cc = CryptoCurrencies(key='RAVFAINVUAJHR2EW', output_format='pandas')

# data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='CNY')
# data['4b. close (USD)'].plot()

# plt.tight_layout()
# plt.title('Daily close value for bitcoin (BTC)')
# plt.grid()
# plt.show()


# ! Foreign Exchange (FX)

# cc = ForeignExchange(key='RAVFAINVUAJHR2EW')

# There is no metadata in this call
# data, _ = cc.get_currency_exchange_rate(from_currency='GBP', to_currency='EUR')

# pprint(data)



