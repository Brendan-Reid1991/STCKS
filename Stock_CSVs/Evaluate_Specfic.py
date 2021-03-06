import numpy as np
import time
import pandas as pd
import sys,os
from plot_module import *

name = sys.argv[1]

def transpose(L):
    return(list(map(list,zip(*L))))


openfile = "All_Stocks/"+name+'.csv'

print(
    'Checking %s'%name
)

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

print(
    '  52 Week High / Low : %.4f / %.4f'%(_52_week_high, _52_week_low)
)

print(
    '  Current price: %.4f'%price_uptodate
)

averages = [50, 150, 200]
rolling_averages = {}
for X in averages:
    avg = sum(closing_price[L - X ::]) / X
    rolling_averages[X] = avg

def pass_fail(idx, R):
    if R not in ['P','p','F','f']:
        raise ValueError('Incorrect pass/fail flag given.')
    if R in ['P','p']:
        result = 'PASS'
    else:
        result = 'FAIL'
    return(
        '    %s -- %s'%(idx, result)
    )

score = 0
# Test 1: Current price above 150- and 200-day averages
if (price_uptodate > rolling_averages[150]) and (price_uptodate > rolling_averages[200]):
    print(pass_fail(1, 'p'))
    score += 1
else:
    print(pass_fail(1, 'f'))

# Test 2: 150- above 200-day average
if rolling_averages[150] > rolling_averages[200]:
    print(pass_fail(2, 'p'))
    score += 1
else:
    print(pass_fail(2, 'f'))

# Test 3: 50-day average is above both 150- and 200-day averages
if (rolling_averages[50] > rolling_averages[200]) and (rolling_averages[50] > rolling_averages[150]):
    print(pass_fail(3, 'p'))
    score += 1
else:
    print(pass_fail(3, 'f'))

# Test 4: Current price is above 50-day average
if price_uptodate > rolling_averages[50]:
    print(pass_fail(4, 'p'))
    score += 1
else:
    print(pass_fail(4, 'f'))

# Test 5: Current price is at least 30% above 52-week low
if price_uptodate >= (1.25 * _52_week_low):
    print(pass_fail(5, 'p'))
    score += 1
else:
    print(pass_fail(5, 'f'))

# Test 6: Current price is within 25% of the 52-week high
if 0.75*_52_week_high <= price_uptodate <= 1.25*_52_week_high:
    print(pass_fail(6, 'p'))
    score += 1
else:
    print(pass_fail(6, 'f'))

print('%s / 6 tests passed.'%score)
