from flask import Flask, request, redirect, jsonify
from gainers import get_yahoo_gainers
from trader import Trader
from trader import Trader
import time
import threading
import math
from queue import Queue
from pprint import pprint
import json
import sys
import os
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
# dt_unix_now = math.floor(time.time())
# dt_unix_pre = 0

# t1 = threading.Thread(target=gainers.get_yahoo_gainers(5))
# t1.dameon = True
# g_gainers = False  
 
# while True:
#     do_stuff()
#     print('helo')
# stocks = Stocks(g_gainers, '60min', 'compact', 60, 100)
# data = stocks.analyze()
# print(data)
# g_gainers = []



# def main(g_gainers):
#     def stockData():
#         if(len(g_gainers) > 0):
#             print('Main')
#             stocks = Stocks(g_gainers, '60min', 'compact', 60, 100)
#             data = stocks.analyze()
#             print(data)
#             time.sleep(60)
#             stockData()
#         else:
#             print('no')
#             time.sleep(10)
#             stockData()
#     stockData()
    
# def gainers():
#         def gainerData():
#             g_gainers = get_yahoo_gainers(5)
#             print(gainers)
#             print(g_gainers)
#             t1 = threading.Thread(target=main(g_gainers))
#             t1.daemon = True
#             t1.start()
#             time.sleep(10)
#             t1.join()
#             gainerData()
#         gainerData()
        
    


# if __name__ == "__main__":
#     gainers()
        
    # print(get_yahoo_gainers(5))

# print(get_yahoo_gainers(5))

# def do_stuff(q):
#     while True:
#         print(q.get())
#         q.task_done()
        
# q = Queue(maxsize=0)
# num_threads = 10

# for x in range(num_threads):
#     worker = threading.Thread(target=do_stuff, args=(q,))
#     worker.daemon = True
#     worker.start()

# for y in range (10):
#     for x in range(100):
#         q.put(x + y * 100)
#     q.join()
#     print("Batch " + str(y) + " Done")
    
# """ waits until the queue is empty and all of the threads are done working 
#  (which it knows because task_done() will have been called on every element of the queue)
# """
buy_and_sell = Trader(interval='60min', outputsize='full', short_window=60, long_window=150, budget=1000)
def gainers(q):
    while True:
        print('Looking up stocks on yahoo')
        q.put(get_yahoo_gainers(15))
        q.task_done()
        time.sleep(30)
        
def stocks(q):
    while True:
        gainers = q.get()
        print('Getting stock data from alpha vantage') # str(threading.currentThread())
        buy_and_sell.trade(gainers)
        # print('Sleeping for 60 seconds')
        # time.sleep(60)
       
q = Queue(maxsize=0)

g_thread = threading.Thread(target=gainers, args=(q,))
g_thread.daemon = True
g_thread.start()
s_thread = threading.Thread(target=stocks, args=(q,))
s_thread.daemon = True
s_thread.start()

while True:
    try: 
        time.sleep(10)
        q.join()
    except KeyboardInterrupt:
        print('Preparing shutdown ...')
        buy_and_sell.createBackup()
        print('Backup created ...')
        try:
            print('Shutting down ...')
            sys.exit(1)
        except SystemExit:
            os._exit(1)