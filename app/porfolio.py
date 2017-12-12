import pandas as pd
import numpy
import pandas_datareader.data as web
# return name and exchange
def getCmpnt(stockList):
    components = []
    for stock in stockList:
        components.append(web.get_components_yahoo(stock))
    return pd.concat(components)

# return PE change_pct    last  short_ratio    time

def getDetail(stockList):
    details = []
    for stock in stockList:
        details.append(web.get_quote_yahoo(stock))
    return pd.concat(details)

# calculate every stock shares
def getShares(stockList, avg, date, df_history):
    shares = {}
    for stock in stockList:
        shares[stock] = avg/df_history[date]['Close'][stock]
    return shares

#porfolio value on a specific day
def getPorfolioValue(stocklist, date, df_history, shares):
    porfolioValue = 0
    for stock in stocklist:
        porfolioValue += df_history[date]['Close'][stock]* shares[stock]
    return porfolioValue

#porfolio value of history
def getPorfolioHistory(stockList, dateList, df_history, shares):
    df_porfolio = {}
    for date in dateList:
        df_porfolio[date] = getPorfolioValue(stockList, date, df_history, shares)
    return df_porfolio






