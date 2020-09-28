import pandas as pd
import numpy as np
from datetime import datetime
import ast,os,time


stock_names = []
for file in os.listdir('Watch/'):
    if file.endswith('.csv'):
        stock_names.append(file[0:-4])

path = 'Watch/'

for s in stock_names:
    csv = pd.read_csv(path + s + '.csv', index_col=0, skip_blank_lines=True)
    indices = list(np.where(csv['Date'].isnull())[0])
    # csv.drop(csv.index[indices])
    # print('    ',len(csv))
    print(csv.index[indices])
