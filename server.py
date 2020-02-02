from flask import Flask, request, redirect, jsonify
from gainers import Gainers
from stock_data import Stocks

app = Flask('python_finance', static_url_path='', static_folder='/src')

@app.route('/')
def hello():
    return jsonify({'response': 'hello'})

@app.route('/gainers')
def gainers():
    g_gainers = Gainers.get_yahoo_gainers(5)
    return {'gainers': g_gainers}

@app.route('/stockdata')
def stocks_data():
    s_gainers = gainers()
    signals = Stocks(s_gainers['gainers'], '60min', 'compact', 60, 100).analyze()
    return str(signals)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='7500')