import numpy as np
import requests
import time
import pandas as pd
import sys,os
from io import BytesIO

test = open('LSE.txt', 'r')
elements = test.readlines()[1:]
equity_stocks = []
for str in elements:
    tab_loc = str.index("\t")
    if tab_loc <= 4:
        equity_stocks.append(
            str[0:tab_loc]
        )

today = int(time.time())
one_year_hence = today - 3600*24*365

success = []
from progress.bar import Bar

def link(stock_name, start_date, end_date):
    return(
        "https://query1.finance.yahoo.com/v7/finance/download/%s.L?period1=%s&period2=%s&interval=1d&events=history"%(stock_name, start_date, end_date)
    )

bar = Bar('Processing...', max = len(equity_stocks), suffix = '%(percent).1f%%')
for x_ in equity_stocks:
    filepath = 'All_Stocks/%s.csv'%x_
    temp_fp  = 'All_Stocks/temp.csv'
    if os.path.exists(filepath):
        existing_csv = pd.read_csv(filepath)#, index_col=0)
        if len(existing_csv.columns) > 7:
            existing_csv = pd.read_csv(filepath, index_col=0)
        
        last_updated = existing_csv['Date'].iloc[-1]
        l = link(x_, one_year_hence, today)
        r = requests.get(l, allow_redirects = True)
        open(temp_fp,'wb').write(r.content)
        new_csv = pd.read_csv(temp_fp)
        idx = new_csv.set_index('Date').index.get_loc(last_updated)
        subframe = new_csv[idx+1::]
        existing_csv = existing_csv.append(
            subframe, ignore_index=True
        )
        existing_csv.to_csv(filepath)
        if os.path.exists(temp_fp):
            os.remove(temp_fp)
    else:
        l = link(x_, one_year_hence, today)

        r = requests.get(l, allow_redirects = True)
        
        if r.ok:
            cr = BytesIO(r.content)
            df = pd.read_csv(cr, sep=',')
            L = len(df)
            c = df["Open"].isnull().sum()
            if pd.isnull(df.iloc[-1]["Open"]) or L == 1 or (c/L > 0.05):
                pass
            else:
                df.to_csv(filepath)
        else:
            # print('nein')
            pass
    bar.next()
bar.finish()