import numpy as np
import time
import pandas as pd
import sys,os

def transpose(L):
    return(list(map(list,zip(*L))))
relevant_data = []
for file in os.listdir('All_Stocks/'):
    if file.endswith('.csv'):
        relevant_data.append(file)

# Averages_50Days = {}
# Averages_150Days = {}
# Averages_200Days = {}
out_file = 'Look_Into.txt'
if os.path.exists(out_file):
    os.remove(out_file)

tally = 0

for filename in sorted(relevant_data):
    openfile = "All_Stocks/"+filename
    name = filename[0:-4]

    # print(
    #     'Checking %s'%name
    # )

    input_csv = pd.read_csv(openfile)

    closing_price = input_csv['Close']
    volume_traded =  input_csv['Volume']
    Dates = input_csv['Date']

    closing_list = list(closing_price)
    
    closing_price = [x for x in closing_list if not pd.isnull(x)]

    price_uptodate = closing_price[-1]

    L = len(closing_price)

    # 52-weeks Highs and Lows
    One_Year_Ish = 52*5
    if L < One_Year_Ish:
        _52_week_low = min(closing_price)
        _52_week_high = max(closing_price)
    else:
        _52_week_low = min(
            closing_price[-One_Year_Ish :: ]
        )
        _52_week_high = max(
            closing_price[-One_Year_Ish :: ]
        )

    # print(
    #     '    52 Week High / Low : %.4f / %.4f'%(_52_week_high, _52_week_low)
    # )

    averages = [50, 150, 200]
    rolling_averages = {}
    for X in averages:
        avg = sum(closing_price[L - X ::]) / X
        rolling_averages[X] = avg


    score = 0
    # Test 1: Current price above 150- and 200-day averages
    if (price_uptodate > rolling_averages[150]) and (price_uptodate > rolling_averages[200]):
        score += 1

    # Test 2: 150- above 200-day average
    if rolling_averages[150] > rolling_averages[200]:
        score += 1

    # Test 3: 50-day average is above both 150- and 200-day averages
    if (rolling_averages[50] > rolling_averages[200]) and (rolling_averages[50] > rolling_averages[150]):
        score += 1
    
    # Test 4: Current price is above 50-day average
    if price_uptodate > rolling_averages[50]:
        score += 1
    
    # Test 5: Current price is at least 30% above 52-week low
    if price_uptodate >= (1.25 * _52_week_low):
        score += 1
    
    # Test 6: Current price is within 25% of the 52-week high
    if 0.75*_52_week_high <= price_uptodate <= 1.25*_52_week_high:
        score += 1
    
    # print('    %s / 6 tests passed.'%score)
    if score >= 4:
        # print('    %s passed the trend template screen.'%name)
        f = open(out_file,"a+")
        f.write('%s\n'%name)
        f.close()
        tally += 1

print(
    '%s stocks passed the template screen'%tally
)