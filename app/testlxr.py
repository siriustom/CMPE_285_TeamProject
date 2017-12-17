stock_info = {
        'Ethical': ('AAPL', 'ADBE', 'NSRGY', 'GILD', 'GOOGL'),
        'Growth': ('BIIB', 'AKRX', 'IPGP', 'PSXP', 'NFLX'),
        'Index': ('VTI', 'IXUS', 'ILTB', 'VIS', 'KRE', 'VEU'),
        'Quality': ('QUAL', 'SPHQ', 'DGRW', 'QDF'),
        'Value': ('AAON', 'CTB', 'JNJ', 'GRUB', 'TTGT')
    }
def get_stock_list(strategy, strategy_ratio):
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