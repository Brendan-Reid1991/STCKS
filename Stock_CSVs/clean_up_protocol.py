import numpy as np
import pandas as pd

import ast,os

import requests

from progress.bar import FillingSquaresBar

stock_names = []
count = 0
removed = 0
bar = FillingSquaresBar(
    message = 'Checking all CSVs',
    suffix = '%(eta_td)s'
)
for file in os.listdir('All_Stocks/'):
    count += 1
    if file.endswith('.csv'):
        imported = pd.read_csv('All_Stocks/' + file)
        check_these = imported['Open'][-100:]
        L = len(list(check_these))
        c = check_these.isnull().sum()
        if c/L > 0.05:
            os.remove('All_Stocks/'+file)
            removed += 1
    
    bar.next()
bar.finish()
print('%s checked; %s removed.'%(count,broken))