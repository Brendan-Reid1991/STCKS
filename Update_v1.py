import pandas as pd
import numpy as np
from datetime import datetime
import ast,os,time

import requests


stock_names = []
for file in os.listdir('Stock_CSVs/'):
    if file.endswith('.csv'):
        stock_names.append(file[0:-4])

current_time_stamp = int(time.time())
seconds_in_30days = 30*24*3600
start_time_stamp = current_time_stamp - seconds_in_30days



def link(stock, start_time, end_time):
    return(
    "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=1%s&interval=1d&events=history"%(stock, start_time, end_time)
    )




for s in stock_names:
    input_csv = pd.read_csv('Stock_CSVs/' + s + '.csv')#, index_col=0)
    if len(input_csv.columns) > 7:
        input_csv = pd.read_csv('Stock_CSVs/' + s + '.csv', index_col=0)
    # else:
        # pd.read_csv('Stock_CSVs/' + s + '.csv')
    
    last_updated = input_csv['Date'].iloc[-1]

    l = link(s, start_time_stamp, current_time_stamp)
    r = requests.get(l, allow_redirects = True)
    open('Stock_CSVs/temp.csv','wb').write(r.content)
    new_csv = pd.read_csv('Stock_CSVs/temp.csv')
    idx = new_csv.set_index('Date').index.get_loc(last_updated)
    subframe = new_csv[idx+1::]
    input_csv = input_csv.append(
        subframe, ignore_index=True
    )
    input_csv.to_csv('Stock_CSVs/' + s + '.csv')
    if os.path.exists('Stock_CSVs/temp.csv'):
        os.remove('Stock_CSVs/temp.csv')
    
