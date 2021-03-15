import pandas as pd
import numpy as np
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import ast,os,time,sys

name = "DDDD.LON"

api = open("AVAPI.txt","r").readlines()[0]

ts = TimeSeries(api)

close = "4. close"
vol = "5. volume"

L = 365

data, meta_data = ts.get_daily(name, outputsize='full')

last_year = np.asarray([item for item in data][0:L])

all_close = []
for date in last_year:
    all_close.append(
        ast.literal_eval(data[date][close])
    )

# print(all_close)

# exit()
averages = [50, 100, 200]
All_Averaged = []
for avg in averages:
    rolling_average = []
    for i in range(L):
        cumulative_price = 0
        incr = 0 
        # print("range", 0 + i , min(avg + i, L - 1))
        for date in last_year[0 + i : min(avg + i, L - 1)]:
            closing_price = ast.literal_eval(data[date][close])
            cumulative_price += closing_price
            incr += 1
        # print("cumulative price", cumulative_price,"increment:",incr)
        rolling_average.append(cumulative_price / max(1,incr))
    All_Averaged.append(rolling_average)

import matplotlib.pyplot as plt
import matplotlib as mpl

# exit()
mpl.style.use('seaborn')
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['axes.linewidth'] = 1.2

nticks = 24
ticks = np.linspace(0, L - 1, nticks, dtype = int)


labels = []
for str in last_year:
    frmt = datetime.strptime(str,'%Y-%m-%d')
    newfrmt = frmt.strftime('%d%b%y')
    labels.append(newfrmt)

labels_ticks = np.asarray(labels)[0:L:20]

w = 15
h = 7
d = 70

plt.figure(figsize=(w, h), dpi=d)

f1 = plt.subplot(1,1,1)
plt.plot(labels[::-1], all_close[::-1], color = 'grey')
plt.xticks(labels_ticks[::-1])
plt.show()
# for idx, X in enumerate(averages):
#     plt.plot(labels, All_Averaged[idx][::-1], label = '%s-day avg'%X)
# plt.setp(f1.get_xticklabels(), visible=False)#input_csv['Date'][ticks], labels, rotation = 30, fontsize = 15)

# plt.legend(fontsize = 18)
# plt.ylabel('Price', fontsize = 18)
# plt.grid(True)

# f2 = plt.subplot(2,1,2, sharex = f1)
# # plt.plot(dates, volume)
# plt.xticks(labels[ticks], labels, rotation = 30, fontsize = 15)
# plt.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
# plt.ylabel('Volume', fontsize = 18)
# plt.tight_layout()
# plt.savefig(name + '.pdf', bbox_inches = 'tight')
