import pandas as pd
import numpy as np
from datetime import datetime
import ast,os

from progress.bar import Bar

relevant_data = []

# Interpolation


all_existing = []
for filename in os.listdir('tempo/'):
    if filename.endswith('.csv'):
        all_existing.append(filename[0:-4])


performing_well = []
Watcher = []
duds = []
bar = Bar('Processing...', max = len(all_existing), suffix = '%(percent).1f%%')
for name in sorted(all_existing):

    filepath = 'tempo/%s.csv'%name

    input_csv = pd.read_csv(filepath)

    blank_prices = list(np.where(input_csv['Close'].isnull())[0])

    # exit()
    L = len(input_csv['Date'])
    if len(blank_prices) > 0:
        if blank_prices[-1] == L - 1:
            blank_prices = blank_prices[0:-2]
    closing_price = list(input_csv['Close'])
    MRP = closing_price[-1]

    volume_traded =  input_csv['Volume']
    Dates = input_csv['Date']


    averages = [150, 200]
    rolling_averages = []

    Lprime = len(blank_prices)
    if Lprime > 0:
        if Lprime == 1:
        #Interpolate
            r_ = blank_prices[0]
            closing_price[r_] = float((closing_price[r_ - 1] + closing_price[r_ + 1]) / 2 )
        elif len(blank_prices) == 2 and np.diff(blank_prices) != 1:
            for _ in blank_prices:
                closing_price[_] = float((closing_price[_ - 1] + closing_price[_ + 1]) / 2 )
        else:
            duds.append([name, len(blank_prices)])
            # print('Multiple missing entries in %s.csv\nNo. missing entries: %s'%(name, len(blank_prices)))
            continue    

    score = 0
    for X in averages:
        init = L - X
        relevant = sum(closing_price[init::])/X
        if relevant > MRP:
            score += 1
    if score == len(averages):
        performing_well.append(name)
        increases = []
        # for xx in averages:
        increase = 100 * MRP/closing_price[L - 200]
        Watcher.append([name, increases])
    bar.next()
bar.finish()

Watcher = sorted(Watcher, key = lambda x : x[1], reverse = True)
print(Watcher[0:5])

print("No. stocks which are ``performing well'':%s"%len(performing_well))


f = open('performing_well_maybe.txt',"w+")
for x in performing_well:
    f.write("%s\n"%x)
f.close()

f = open('duds_maybe.txt',"w+")
for x in duds:
    f.write("%s\n"%x)
f.close()


averages_to_plot = []
for good_stock in performing_well:
    filepath = 'tempo/%s.csv'%good_stock
    
    input_csv = pd.read_csv(filepath)

    blank_prices = list(np.where(input_csv['Close'].isnull())[0])

    L = len(input_csv['Date'])
    if len(blank_prices) > 0:
        if blank_prices[-1] == L - 1:
            blank_prices = blank_prices[0:-2]
    closing_price = list(input_csv['Close'])
    MRP = closing_price[-1]

    volume_traded =  input_csv['Volume']
    Dates = input_csv['Date']


    averages = [200]
    rolling_averages = []

    Lprime = len(blank_prices)
    if Lprime > 0:
        if Lprime == 1:
        #Interpolate
            r_ = blank_prices[0]
            closing_price[r_] = float((closing_price[r_ - 1] + closing_price[r_ + 1]) / 2 )
        elif len(blank_prices) == 2 and np.diff(blank_prices) != 1:
            for _ in blank_prices:
                closing_price[_] = float((closing_price[_ - 1] + closing_price[_ + 1]) / 2 )
    rolling_average = []
    for X in averages:
        temp = []
        cum_price = 0
        for idx, price in enumerate(closing_price[0:X]):
            cum_price += price
            avg = cum_price / (idx+1)
            temp.append(avg)
        rolling_average.append(temp)
    for idx, X in enumerate(averages):
        i = 1
        end = 0
        while end < L:
            start = 0 + i
            end = X + i
            r_a = sum(closing_price[start:end]) / X
            rolling_average[idx].append(r_a)
            i+=1
    averages_to_plot.append(
        rolling_average
    )

import matplotlib.pyplot as plt

for x_ in averages_to_plot:
    plt.plot(x_)

plt.savefig('test.png')
