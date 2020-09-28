import pandas as pd
import numpy as np
from datetime import datetime
import ast,os,time


stock_names = []
for file in os.listdir('Watch/'):
    if file.endswith('.csv'):
        stock_names.append(file[0:-4])
