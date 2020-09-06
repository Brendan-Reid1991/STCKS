import pandas as pd
import numpy as np
from datetime import datetime
import ast,os

relevant_data = []

# Interpolation

openfile = 'tempo/ABF.csv'
name = 'ABF'

input_csv = pd.read_csv(openfile)

blank_prices = list(np.where(input_csv['Close'].isnull())[0])
print(blank_prices)
# exit()
L = len(input_csv['Date'])

closing_price = list(input_csv['Close'])
volume_traded =  input_csv['Volume']
Dates = input_csv['Date']


averages = [100, 150, 200]
rolling_averages = []



if len(blank_prices) == 1:
    #Interpolate
    r_ = blank_prices[0]
    xa = float((closing_price[r_ - 1] + closing_price[r_ + 1]) / 2 )
else:
    print('Multiple missing entries in %s.csv\nNo. missing entries: %s'%(name, len(blank_prices)))
    # continue    


for X in averages:
    temp = []
    cum_price = 0
    for idx, price in enumerate(closing_price[0:X]):
        cum_price += price
        avg = cum_price / (idx+1)
        temp.append(avg)
    rolling_averages.append(temp)
for idx, X in enumerate(averages):
    i = 1
    end = 0
    while end < L:
        start = 0 + i
        end = X + i
        r_a = sum(closing_price[start:end]) / X
        rolling_averages[idx].append(r_a)
        i+=1

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('seaborn')
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['axes.linewidth'] = 1.2


nticks = 12
ticks = np.linspace(0, L - 1, nticks, dtype = int)

labels = []
for str in input_csv['Date'][ticks]:
    frmt = datetime.strptime(str,'%Y-%m-%d')
    newfrmt = frmt.strftime('%d %b %y')
    labels.append(newfrmt)

w = 15
h = 7
d = 70

plt.figure(figsize=(w, h), dpi=d)

f1 = plt.subplot(2,1,1)
plt.plot(Dates, closing_price, color = 'grey')
for idx, X in enumerate(averages):
    plt.plot(Dates, rolling_averages[idx], label = '%s-day avg'%X)
plt.setp(f1.get_xticklabels(), visible=False)#input_csv['Date'][ticks], labels, rotation = 30, fontsize = 15)

plt.legend(fontsize = 18)
plt.ylabel('Price', fontsize = 18)
plt.grid(True)

f2 = plt.subplot(2,1,2, sharex = f1)
plt.plot(Dates, input_csv['Volume'])
plt.xticks(Dates[ticks], labels, rotation = 30, fontsize = 15)
plt.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
plt.ylabel('Volume', fontsize = 18)
plt.tight_layout()
plt.savefig(name + '.pdf', bbox_inches = 'tight')