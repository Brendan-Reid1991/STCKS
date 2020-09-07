import numpy as np
import pandas as pd

import ast,os

import requests


stock_names = []
count = 0
broken = 0
for file in os.listdir('All_Stocks/'):
    count += 1
    if file.endswith('.csv'):
        imported = pd.read_csv('All_Stocks/' + file)
        check_these = imported['Open'][-100:]
        L = len(list(check_these))
        c = check_these.isnull().sum()
        if c/L > 0.05:
            os.remove('All_Stocks/'+file)
            broken += 1
print('%s removed.'%count)