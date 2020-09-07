import pandas as pd
import numpy as np
from datetime import datetime
import ast,os,time,sys

import requests

name = sys.argv[1]

current_time_stamp = int(time.time())
start_time_stamp = current_time_stamp - 3600*24*365



def link(stock, start_time, end_time):
    return(
    "https://query1.finance.yahoo.com/v7/finance/download/%s.L?period1=%s&period2=1%s&interval=1d&events=history"%(stock, start_time, end_time)
    )

l = link(name, start_time_stamp, current_time_stamp)
r = requests.get(l, allow_redirects = True)
if r.ok:
    open('Watch/%s.csv'%name,'wb').write(r.content)
else:
    print('Link invalid')
