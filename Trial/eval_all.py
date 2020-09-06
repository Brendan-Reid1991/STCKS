import numpy as np
import time
import pandas as pd
import sys,os

def transpose(L):
    return(list(map(list,zip(*L))))
relevant_data = []
for file in os.listdir('tempo/'):
    if file.endswith('.csv'):
        relevant_data.append(file)

Averages_150Days = {}
Averages_200Days = {}

for filename in relevant_data:
    openfile = "tempo/"+filename
    name = filename[0:-4]

    input_csv = pd.read_csv(openfile)

    closing_price = input_csv['Close']
    volume_traded =  input_csv['Volume']
    Dates = input_csv['Date']

    closing_list = list(closing_price)
    
    closing_price = [x for x in closing_list if not pd.isnull(x)]

    averages = [150, 200]
    rolling_averages = []

    price_uptodate = closing_price[-1]
    L = len(closing_price)

    rolling_averages = []
    for X in averages:
        avg = sum(closing_price[L - X ::]) / X
        rolling_averages.append(avg)
    score = 0
    if price_uptodate > rolling_averages[0]:
        score += 1
    if price_uptodate > rolling_averages[1]:
        score += 1
    if score == 2:
        print(name, price_uptodate,'|',rolling_averages)