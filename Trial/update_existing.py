import numpy as np
import requests
import time
import pandas as pd
import sys,os
from io import BytesIO

from progress.bar import Bar

def link(stock_name, start_date, end_date):
    return(
        "https://query1.finance.yahoo.com/v7/finance/download/%s.L?period1=%s&period2=%s&interval=1d&events=history"%(stock_name, start_date, end_date)
    )

today = int(time.time())
one_year_hence = today - 3600*24*365

all_existing = []
for filename in os.listdir('tempo/'):
    if filename.endswith('.csv'):
        all_existing.append(filename[0:-4])

bar = Bar('Processing...', max = len(all_existing), suffix = '%(percent).1f%%')
for x_ in all_existing:
    filepath = 'tempo/%s.csv'%x_

    existing_csv = pd.read_csv('tempo/' + x_ + '.csv')#, index_col=0)
    if len(existing_csv.columns) > 7:
        existing_csv = pd.read_csv('tempo/' + x_ + '.csv', index_col=0)
    
    last_updated = existing_csv['Date'].iloc[-1]
    l = link(x_, one_year_hence, today)
    r = requests.get(l, allow_redirects = True)
    if r.ok:
        open('tempo/temp.csv','wb').write(r.content)
        new_csv = pd.read_csv('tempo/temp.csv')
        if new_csv.empty:
            os.remove(filepath)
            print('\nRemoved %s'%x_)
            pass
        else:
            idx = new_csv.set_index('Date').index.get_loc(last_updated)
            subframe = new_csv[idx+1::]
            existing_csv = existing_csv.append(
                subframe, ignore_index=True
            )
            existing_csv.to_csv(filepath)
    if os.path.exists('tempo/temp.csv'):
        os.remove('tempo/temp.csv')
        bar.next()
bar.finish()