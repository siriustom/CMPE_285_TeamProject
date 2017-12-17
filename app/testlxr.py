import urllib2
import csv
import numpy as np, numpy.random
import datetime

stock_info = {
        'Ethical': ('AAPL', 'ADBE', 'NSRGY', 'GILD', 'GOOGL'),
        'Growth': ('BIIB', 'AKRX', 'IPGP', 'PSXP', 'NFLX'),
        'Index': ('VTI', 'IXUS', 'ILTB', 'VIS', 'KRE', 'VEU'),
        'Quality': ('QUAL', 'SPHQ', 'DGRW', 'QDF'),
        'Value': ('AAON', 'CTB', 'JNJ', 'GRUB', 'TTGT')
    }

symbol_map = {}

API_KEY = '2IGI5KM2OW30BC4P'
API_BASE_CURRENT = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&apikey={}&symbol={}&interval=1min' \
                   '&datatype=csv'

def load_symbol_map(fname):
    with open(fname, 'rb') as fp:
        reader = csv.reader(fp)
        stock_exchange = fname.split('.')[0]
        next(reader, None)  # skip the header
        for row in reader:
            symbol_map[row[0]] = [row[1], stock_exchange]

def prepare_symbols():
    load_symbol_map('nasdaq.csv')
    load_symbol_map('nyse.csv')
    load_symbol_map('amex.csv')

def get_share_lastday(stock_short):
    API_KEY = '2IGI5KM2OW30BC4P'
    API_BASE_DAILY = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey={}&symbol={}&datatype=csv'
    stock_short = stock_short.upper()
    response = urllib2.urlopen(API_BASE_DAILY.format(API_KEY, stock_short))

    reader = csv.reader(response)
    next(reader, None)  # skip the header
    ts_data = [row for row in reader]
    return ts_data[:1]  # return last data

def get_change(data):
    open = float(data[0][1])
    close = float(data[0][3])
    return close - open

def get_stock_list(strategy):
    #define the stocks for each strategy
    stocks = stock_info[strategy]

    change_name = [(float(get_change(get_share_lastday(name))), name) for name in stocks]
    change_name.sort(key=lambda x: -x[0])

    top_stocks = [change_name[i][1] for i in xrange(3)] #select the top3 stocks
    #get random ratio of stock
    random_ratio = np.mean(np.random.dirichlet(np.ones(3), 10), axis=0).tolist()
    # the stocks_list for the selected strategies
    stock_percent_list={}
    for i in range(0,len(top_stocks)):
        stock_percent_list[stocks[i]]= random_ratio[i]
    return stock_percent_list

print(get_stock_list('Ethical'))

def get_current_stock_info(stock_short):
    stock_short = stock_short.upper()
    stock_share = urllib2.urlopen(API_BASE_CURRENT.format(API_KEY, stock_short))

    # stock_share = Share(stock_short)
    reader = csv.reader(stock_share)
    next(reader, None)  # skip header: timestamp,open,high,low,close,volume
    latest = next(reader, None)
    stock_current_info = {}
    stock_current_info['stock_short'] = stock_short
    # timestamp format: 2017-12-15 16:00:00
    stock_trade_datetime = datetime.datetime.strptime(latest[0], '%Y-%m-%d %H:%M:%S')
    # use close price
    stock_latest_price = latest[4]
    # stock_latest_price=stock_share.get_price()
    stock_current_info['stock_latest_price'] = stock_latest_price
    stock_current_info['stock_trade_datetime'] = stock_trade_datetime

    # lazy load symbols map
    if not symbol_map:
        prepare_symbols()

    stock_current_info['stock_exchange'] = symbol_map[stock_short][1]
    stock_current_info['stock_company_name'] = symbol_map[stock_short][0]
    return stock_current_info

print(get_current_stock_info('AAPL'))