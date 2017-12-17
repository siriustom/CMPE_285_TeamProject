from app.PickStrategies import get_stock_list_all, get_strategy_stock_info, get_historical_strategy_stock_value
from flask import render_template, flash, redirect, request
from app import app
from .forms import InvestForm
import json


@app.route('/invest', methods=['GET', 'POST'])
def invest():
    form = InvestForm(request.form)
    if request.method =='POST':
        try:
            form = InvestForm(request.form)
            amount = float(request.form['amount'])
            print(1)
            if amount < 5000:
                print('fucccccccccccccc')
                return render_template('error.html')
            print(2)
            print(amount)
            choices = request.form.getlist('strategies')
            print(3)
            if len(choices)<=0 or len(choices)>2:
                return render_template('error.html')
            print(choices)
            print(4)
            testArray = ['Ethical']
            stocklist = get_stock_list_all(testArray)
            print(stocklist.keys())
            testlist = {'ISRG': 0.3469070257097072, 'AAPL': 0.3548278127860295, 'ADBE': 0.29826516150426335}
            details = get_strategy_stock_info(testlist, amount)
            print(6)
            print(stocklist)
            print('1234')
            history = get_historical_strategy_stock_value(stocklist, amount)
            print(7)
            print(history)
            return render_template("result.html", details=details, history=history)
            #return render_template("result.html", details=details, data=map(json.dumps, details))

        except:
            return render_template('error.html')

    return render_template('invest.html', form=form,
                           strategy=app.config['STRATEGY'])

