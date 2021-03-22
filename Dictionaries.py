import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import ast,os,time,sys
from progress.bar import ShadyBar


api = open("AVAPI.txt","r").readlines()[0]

ts = TimeSeries(api)

def save_obj(obj, name):
    with open('dicts/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('dicts/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

test = open('LSE.txt', 'r')
elements = test.readlines()[1:]

equity_stocks = []
for str in elements:
    
    try:
        tab_loc = str.index("\t")
    except ValueError:
        tab_loc = len(str)

    equity_stocks.append(
        str[0:tab_loc]
    )

L_All = len(equity_stocks)


removals = []
bar = ShadyBar('Attempting to get dictionaries:', max = len(equity_stocks), suffix = '%(percent).2f%%')
for idx, ticker in enumerate(equity_stocks):
    if os.path.exists("dicts/" + ticker + ".pkl"):
        bar.next()
        continue
    else:
        try:
            data, meta_data = ts.get_daily(ticker + ".LON", outputsize='full')
            save_obj(data, ticker)
        except ValueError:
            removals.append(ticker)
            pass
        bar.next()
bar.finish()

equity_stocks = [x for x in equity_stocks if x not in removals]

rewrite = open("LSE_updated.txt", "w")
for stock in equity_stocks:
    rewrite.write(stock + "\n")



