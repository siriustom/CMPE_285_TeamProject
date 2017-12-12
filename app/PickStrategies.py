#get history information of an stock
from yahoo_finance import Share
from collections import defaultdict, OrderedDict
import datetime
import pandas as pd
import pandas_datareader.data as pdr
import json
import numpy as np, numpy.random


# get history_stock_info for stock_name

def get_historical_info_pandas(stock_short):
    date_time_current = datetime.datetime.now().date()
    # get the date of 7 days ago
    date_gap = datetime.timedelta(days=30)
    date_time_sevendays_ago = date_time_current - date_gap
    # history for 7 days
    stock_history_frame = pdr.DataReader(stock_short,'google',str(date_time_sevendays_ago),str(date_time_current))
    df=pd.DataFrame(stock_history_frame)
    close_df=df.get('Close')
    tk=close_df.index.tolist()[-5:]

    close_price_dic=close_df.to_dict()
    stock_history = [(ts.strftime("%Y-%m-%d"), close_price_dic[ts]) for ts in tk]
    return stock_history


def get_historical_info(stock_short):
    stock_share=Share(stock_short)
    date_time_current= datetime.datetime.now().date()
    #get the date of 7 days ago
    date_gap=datetime.timedelta(days=7)
    date_time_sevendays_ago = date_time_current-date_gap
    #history for 7 days
    stock_history = stock_share.get_historical(str(date_time_sevendays_ago), str(date_time_current))
    return stock_history

# get the current info of the latest stock info from yahoo_finance
def get_current_stock_info(stock_short):
    stock_share = Share(stock_short)
    stock_current_info={}
    stock_current_info['stock_short']=stock_short
    stock_latest_price=stock_share.get_price()
    stock_current_info['stock_latest_price']=stock_latest_price
    stock_trade_datetime = stock_share.get_trade_datetime()
    stock_current_info['stock_trade_datetime'] = stock_trade_datetime
    stock_exchange = stock_share.get_stock_exchange()
    stock_current_info['stock_exchange'] = stock_exchange
    stock_company_name = stock_share.get_name()
    stock_current_info['stock_company_name'] = stock_company_name
    return stock_current_info


# get all the stock list and according percentage for the selected strategies
def get_stock_list_all(strategy_list):
    stock_percent_list={}
    if(len(strategy_list)==1):
        stock_percent_list=get_stock_list(strategy_list[0],1)
    else:
        for strategy in strategy_list:
            stock_percent_list.update(get_stock_list(strategy,0.5))
    return stock_percent_list


stock_info = {
        'Ethical': ('AAPL', 'ADBE', 'NSRGY', 'GILD', 'GOOGL'),
        'Growth': ('BIIB', 'AKRX', 'IPGP', 'PSXP', 'NFLX'),
        'Index': ('VTI', 'IXUS', 'ILTB', 'VIS', 'KRE', 'VEU'),
        'Quality': ('QUAL', 'SPHQ', 'DGRW', 'QDF'),
        'Value': ('AAON', 'CTB', 'JNJ', 'GRUB', 'TTGT')
    }
#get the stock list and according percentage for one selected strategy, and the allotment is divided equally
def get_stock_list(strategy,strategy_ratio):
    #define the stocks for each strategy
    stocks = stock_info[strategy]
    change_name = [(float(Share(name).get_change()), name) for name in stocks]
    change_name.sort(key=lambda x: -x[0])
    top_stocks = [change_name[i][1] for i in xrange(3)] #select the top3 stocks
    #get random ratio of stock
    random_ratio = np.mean(np.random.dirichlet(np.ones(3), 10), axis=0).tolist()
    # the stocks_list for the selected strategies
    stock_percent_list={}
    for i in range(0,len(top_stocks)):
        stock_percent_list[stocks[i]]= random_ratio[i] * strategy_ratio
    return stock_percent_list


#investment for each stock info,the value is  five days ago(work time, not including weekends)
def get_strategy_stock_info(stock_list,investment):
    #stock_list={}
    #stock_list['AAPL']=0.5
    #stock_list['ADBE'] = 0.5
    #investment=5000
    stock_strategy_invest_info={}
    for stock_short in stock_list:
        stock_current_info=get_current_stock_info(stock_short)
        holding_ratio=stock_list[stock_short]
        stock_current_info['holding_ratio']=float("{0:.4f}".format(holding_ratio))
        stock_current_info['holding_value'] = float("{0:.2f}".format(holding_ratio*investment))
        stock_strategy_invest_info[stock_short]=stock_current_info
    return stock_strategy_invest_info


#get the portfolio total value of the past five days--dict
def get_historical_strategy_stock_value1(stock_list,investment):
    stock_historical_values= defaultdict(float)
    ordered_date = []
    for stock_short in stock_list:
        historical_info=get_historical_info_pandas(stock_short)
        if not ordered_date:
            ordered_date = [itm[0] for itm in historical_info]
        holding_ratio = stock_list[stock_short]
        point_price=historical_info[0][1]
        for i in range(0,5):
            stock_historical_values[historical_info[i][0]]+= historical_info[i][1]/point_price*investment*holding_ratio
    dict_json = OrderedDict()
    for date in ordered_date:
        dict_json[date] = stock_historical_values[date]
    json_str = json.dumps(dict_json)

    return json_str

#get the portfolio total value of the past five days--dict
def get_historical_strategy_stock_value(stock_list,investment):
    stock_historical_values= defaultdict(float)
    ordered_date = []
    for stock_short in stock_list:
        historical_info=get_historical_info_pandas(stock_short)
        print("======================")
        print(historical_info)
        if not ordered_date:
            ordered_date = [itm[0] for itm in historical_info]
        holding_ratio = stock_list[stock_short]
        point_price=historical_info[0][1]
        for i in xrange(5):
            stock_historical_values[historical_info[i][0]]+= historical_info[i][1]/point_price*investment*holding_ratio
    result = []
    for date in ordered_date:
        dict_json = {}
        dict_json['date'] = date
        dict_json['value'] = float("{0:.2f}".format(stock_historical_values[date]))
        result.append(dict_json)
    #json_str = json.dumps(dict_json)
    print(len(result))
    return result
