
from collections import defaultdict, OrderedDict
import datetime
import numpy as np, numpy.random
import urllib2
import csv


API_KEY = '2IGI5KM2OW30BC4P'
API_BASE_CURRENT = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&apikey={}&symbol={}&interval=1min' \
                   '&datatype=csv'
API_BASE_DAILY = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey={}&symbol={}&datatype=csv'

symbol_map = {}

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

def get_historical_info(stock_short):
    stock_short = stock_short.upper()
    response = urllib2.urlopen(API_BASE_DAILY.format(API_KEY, stock_short))

    reader = csv.reader(response)
    next(reader, None)  # skip the header
    ts_data = [row for row in reader]
    return ts_data[:7]  # return last 7days' data

# get the current info of the latest stock info from alphavantage
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


# get all the stock list and according percentage for the selected strategies
def get_stock_list_all(strategy_list):
    stock_percent_list={}
    if(len(strategy_list)==1):
        stock_percent_list=get_stock_list(strategy_list[0], 1)
    else:
        for strategy in strategy_list:
            stock_percent_list.update(get_stock_list(strategy, 0.5))
    return stock_percent_list


stock_info = {
        'Ethical': ('CECE', 'CSOD', 'PESI', 'POPE', 'SMED'),
        'Growth': ('TSLA', 'AVAV', 'TATT', 'SIFY', 'KLXI'),
        'Index': ('LNDC', 'LWAY', 'MDLZ', 'RAVE', 'RIBT'),
        'Quality': ('RYAAY', 'SABR', 'TST', 'EDBI', 'AFMD')
    }
#get the stock list and according percentage for one selected strategy, and the allotment is divided equally
def get_stock_list(strategy, strategy_ratio):
    #define the stocks for each strategy
    stocks = stock_info[strategy]

    change_name = [(float(get_change(get_share_lastday(name))), name) for name in stocks]
    change_name.sort(key=lambda x: -x[0])

    top_stocks = [change_name[i][1] for i in xrange(3)] #select the top3 stocks
    #get random ratio of stock
    random_ratio = np.mean(np.random.dirichlet(np.ones(3), 10), axis=0).tolist()
    # the stocks_list for the selected strategies
    stock_percent_list = {}
    for i in range(0,len(top_stocks)):
        stock_percent_list[stocks[i]]= random_ratio[i] * strategy_ratio
    return stock_percent_list


#investment for each stock info,the value is  five days ago(work time, not including weekends)
def get_strategy_stock_info(stock_list, investment):
    stock_strategy_invest_info = {}
    for stock_short in stock_list:
        stock_current_info = get_current_stock_info(stock_short) #get every current stock info
        holding_ratio = stock_list[stock_short]
        stock_current_info['holding_ratio'] = float("{0:.4f}".format(holding_ratio))
        stock_current_info['holding_value'] = float("{0:.2f}".format(holding_ratio * investment))
        # fill stock combination of current strategy with current stock info
        stock_strategy_invest_info[stock_short] = stock_current_info
    return stock_strategy_invest_info


#get the portfolio total value of the past five days--dict
def get_historical_strategy_stock_value(stock_list, investment):
    stock_historical_values = defaultdict(float)
    ordered_date = []
    result = []
    for stock_short in stock_list:
        historical_info = get_historical_info(stock_short)
        if not ordered_date:
            ordered_date = [itm[0] for itm in historical_info]
        holding_ratio = stock_list[stock_short]
        point_price = float(historical_info[0][4])
        for i in range(0, 7):
            stock_historical_values[historical_info[i][0]] += float(historical_info[i][4])\
                                                              / point_price * investment * holding_ratio

    for date in ordered_date:
        dict_json = {}
        dict_json['date'] = date
        dict_json['value'] = float("{0:.2f}".format(stock_historical_values[date]))
        result.append(dict_json)
    return result

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
