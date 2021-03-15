import pandas as pd
import numpy as np
from datetime import datetime
import ast,os,time


stock_names = []
for file in os.listdir('Watch/'):
    if file.endswith('.csv'):
        stock_names.append(file[0:-4])

path = 'Watch/'

# Erroneous Lines
for s in stock_names:
    csv = pd.read_csv(path + s + '.csv', index_col=0)
    indices = list(np.where(csv['Close'].isnull())[0])
    if len(indices) == 0:
        continue
    else:
        csv.drop(csv.index[indices], inplace = True)
        csv.to_csv(path + s + '.csv')

# Duplicate Lines
for s in stock_names:
    csv = pd.read_csv(path + s + '.csv', index_col=0, skip_blank_lines=True)
    duplicates = csv[csv.duplicated(['Date'])].index
    if len(duplicates) == 0:
        continue
    else:
        csv.drop(csv.index[duplicates], inplace = True)
        csv.index = range(len(csv))
        csv.to_csv(path + s + '.csv')

Incorrect_Dates = ['2020-09-16', '2020-09-17']
Fix_Columns = ['Open', 'High', 'Low', 'Close', 'Adj. Close']
for s in stock_names:
    csv = pd.read_csv(path + s + '.csv', index_col=0, skip_blank_lines=True)
    for date in Incorrect_Dates:
        for c_name in Fix_Columns:
            a = float(csv.loc[csv['Date'] == date][c_name])
            csv.loc[csv['Date'] == date, c_name] = 10*a
    csv.to_csv(path + s + '.csv')