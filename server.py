from flask import Flask, request, redirect, jsonify
from gainers import get_yahoo_gainers
from stock_data import Stocks
import time
import threading
import math

# app = Flask('python_finance', static_url_path='', static_folder='/src')

# @app.route('/')
# def hello():
#     return jsonify({'response': 'hello'})

# @app.route('/gainers')
# def gainers():
#     print(time.time())
#     g_gainers = Gainers.get_yahoo_gainers(5)
#     return {'gainers': g_gainers}

# @app.route('/stockdata')
# def stocks_data():
#     s_gainers = gainers()
#     signals = Stocks(s_gainers['gainers'], '60min', 'compact', 60, 100).analyze()
#     return str(signals)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='7500')


# def do_stuff():
#     if g_gainers == False:
#         g_gainers = gainers.get_yahoo_gainers(5)
#     elif dt_unix_now - dt_unix_pre > 10:
#         t1.start()
            
#         # print(g_gainers)
dt_unix_now = math.floor(time.time())
dt_unix_pre = 0

# t1 = threading.Thread(target=gainers.get_yahoo_gainers(5))
# t1.dameon = True
# g_gainers = False  
 
# while True:
#     do_stuff()
#     print('helo')
# stocks = Stocks(g_gainers, '60min', 'compact', 60, 100)
# data = stocks.analyze()
# print(data)
g_gainers = []

def gainers():
        def gainerData():
            g_gainers = get_yahoo_gainers(5)
            print(gainers)
            print(g_gainers)
            time.sleep(10)
            gainerData()
        gainerData()
        
t1 = threading.Thread(target=gainers())
t1.daemon = True

def main():
    def stockData():
        if(len(g_gainers) > 0):
            print('Main')
            print(g_gainers)
            stocks = Stocks(g_gainers, '60min', 'compact', 60, 100)
            time.sleep(60)
            stockData()
        else:
            time.sleep(10)
            stockData()
    
if __name__ == "__main__":
    main()
    t1.start()
 
        
    # print(get_yahoo_gainers(5))

# print(get_yahoo_gainers(5))