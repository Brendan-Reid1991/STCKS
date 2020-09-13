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


report_me = 'report.txt'
if os.path.exists(report_me):
    os.remove(report_me)

# removal = 'removed.txt'
# if os.path.exists(removal):
#     os.remove(removal)
# if os.path.exists('faulty_link.txt'):
#     os.remove('faulty_link.txt')


bar = Bar('Processing stock data:', max = len(equity_stocks), suffix = '%(percent).1f%%')
for x_ in equity_stocks:
    # print(x_)
    filepath = 'All_Stocks/%s.csv'%x_
    temp_fp  = 'All_Stocks/temp.csv'
    if os.path.exists(filepath):
        existing_csv = pd.read_csv(filepath)#, index_col=0)
        if len(existing_csv.columns) > 7:
            existing_csv = pd.read_csv(filepath, index_col=0)
        
        last_updated = existing_csv['Date'].iloc[-1]
        l = link(x_, one_year_hence, today)
        r = requests.get(l, allow_redirects = True)
        if r.ok:
            pass
        else:
            g = open(report_me,"a+")
            g.write('%s :: Link no longer working; CSV removed\n'%x_)
            g.close()
            os.remove(filepath)
            continue
        open(temp_fp,'wb').write(r.content)
        new_csv = pd.read_csv(temp_fp)
        idx = new_csv.set_index('Date').index.get_loc(last_updated)
        subframe = new_csv[idx+1::]
        existing_csv = existing_csv.append(
            subframe, ignore_index=True
        )
        existing_csv.to_csv(filepath)
        g = open(report_me,"a+")
        g.write('%s :: Existing CSV updated\n'%x_)
        g.close()
        if os.path.exists(temp_fp):
            os.remove(temp_fp)
    else:
        l = link(x_, one_year_hence, today)

        r = requests.get(l, allow_redirects = True)
        cr = BytesIO(r.content)
        df = pd.read_csv(cr, sep=',')
        L = len(df)
        if r.ok and L > 1:
            c = df["Open"].isnull().sum()
            if pd.isnull(df.iloc[-1]["Open"]) or L == 1 or (c/L > 0.05):
                pass
            else:
                df.to_csv(filepath)
                g = open(report_me,"a+")
                g.write('%s :: CSV downloaded\n'%x_)
                g.close()
        else:
            g = open(report_me,"a+")
            g.write('%s :: Link faulty; skipping\n'%x_)
            g.close()

    bar.next()
bar.finish()