import pandas as pd
import numpy as np
from datetime import datetime
import ast,os
from plot_module import *

relevant_data = []
for file in os.listdir('Watch/'):
    if file.endswith('.csv'):
        relevant_data.append(file)

print("\nPick a CSV file.")
i = 0
for file in relevant_data:
    print(i, "-",file)
    i += 1 
print(i, "- All")
q = input()
if int(q) == len(relevant_data):
    for filename in relevant_data:
        openfile = "Stock_CSVs/"+filename
        name = filename[0:-4]

        input_csv = pd.read_csv(openfile)


        L = len(input_csv['Date'])

        closing_price = input_csv['Close']
        volume_traded =  input_csv['Volume']
        Dates = input_csv['Date']


        averages = [50, 150, 200]
        rolling_averages = []

        blank_prices = list(np.where(closing_price.isnull())[0])
        closing_price = list(closing_price)    
        for r_ in blank_prices:
            if r_ == len(closing_price):
                break
            
            closing_price[r_] = float((closing_price[r_ - 1] + closing_price[r_ + 1]) / 2 )

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

        plot_graph(name, Dates, closing_price, volume_traded, rolling_averages)
else:
    file = "Stock_CSVs/"+relevant_data[int(q)]
    name = relevant_data[int(q)][0:-4]

    input_csv = pd.read_csv(file)


    L = len(input_csv['Date'])

    closing_price = input_csv['Close']
    volume_traded =  input_csv['Volume']
    Dates = input_csv['Date']


    averages = [100, 150, 200]
    rolling_averages = []
    
    blank_prices = list(np.where(closing_price.isnull())[0])
    closing_price = list(closing_price)
    for r_ in blank_prices:
        closing_price[r_] = float((closing_price[r_ - 1] + closing_price[r_ + 1]) / 2 )
        
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

    plot_graph(name, Dates, closing_price, volume_traded, rolling_averages)