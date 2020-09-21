import numpy as np
import requests
import time
import pandas as pd
import sys,os
from io import BytesIO

stock_names = []
for file in os.listdir('All_Stocks/'):
    if file.endswith('.csv'):
        stock_names.append(file[0:-4])

L = len(stock_names)

today = int(time.time())
six_months = today - 3600*24*365*0.5

success = []
from progress.bar import Bar

def link(stock_name, start_date, end_date):
    return(
        "https://query1.finance.yahoo.com/v7/finance/download/%s.L?period1=%s&period2=%s&interval=1d&events=history"%(stock_name, start_date, end_date)
    )


report_me = 'report.txt'
if os.path.exists(report_me):
    os.remove(report_me)

updated = 0
up_to_date = 0
failed = 0
bar = Bar('Processing stock data:', max = len(stock_names), suffix = '%(percent).1f%%')
for idx,x_ in enumerate(stock_names):

    write_me = '%s:\n'%x_
    filepath = 'All_Stocks/%s.csv'%x_
    temp_fp  = 'All_Stocks/temp.csv'

    existing_csv = pd.read_csv(filepath, sep=',')#, index_col=0)
    if len(existing_csv.columns) > 7:
        existing_csv = pd.read_csv(filepath, index_col=0, sep=',')
    
    last_updated = existing_csv['Date'].iloc[-1]
    l = link(x_, six_months, today)
    r = requests.get(l, allow_redirects = True)
    if r.ok:
        pass
    else:
        write_me += '    >Link no longer working\n'
        failed += 1
        # os.remove(filepath)
        continue
    write_me += '    >Link working....'
    open(temp_fp,'wb').write(r.content)
    new_csv = pd.read_csv(temp_fp, sep=',')
    idx = new_csv.set_index('Date').index.get_loc(last_updated)
    if idx == len(new_csv):
        write_me += '     >CSV up-to-date.\n'
        up_to_date += 1
        continue
    else:
        subframe = new_csv[idx+1::]
        existing_csv = existing_csv.append(
            subframe, ignore_index=True
        )
        existing_csv.to_csv(filepath)
        write_me += 'CSV updated\n'
        updated += 1
    # write_me+= '\n'
    g = open(report_me,"a+")
    g.write(write_me)
    g.close()
    bar.next()
bar.finish()
print('\n%s equity tickers tested; %s updated, %s up-to-date, %s links failed.'%(L, updated, up_to_date, failed))