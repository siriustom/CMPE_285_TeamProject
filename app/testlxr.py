import urllib2
import csv
stock_info = {
        'Ethical': ('AAPL', 'ADBE', 'NSRGY', 'GILD', 'GOOGL'),
        'Growth': ('BIIB', 'AKRX', 'IPGP', 'PSXP', 'NFLX'),
        'Index': ('VTI', 'IXUS', 'ILTB', 'VIS', 'KRE', 'VEU'),
        'Quality': ('QUAL', 'SPHQ', 'DGRW', 'QDF'),
        'Value': ('AAON', 'CTB', 'JNJ', 'GRUB', 'TTGT')
    }

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