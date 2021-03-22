import numpy as np
import time
import pandas as pd
import sys,os,pickle,ast


def save_obj(obj, name):
    with open('dicts/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('dicts/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def transpose(L):
    return(list(map(list,zip(*L))))


close = "4. close"

relevant_data = []
for file in os.listdir('dicts/'):
    if file.endswith('.pkl'):
        relevant_data.append(file[0:-4])

out_file = 'Prospective.txt'
if os.path.exists(out_file):
    os.remove(out_file)

tally = 0
results = []
for name in sorted(relevant_data):
    stock_dict = load_obj(name)
    One_Year_Ish = 52*5
    
    closing_price = []
    for key in stock_dict:
        closing_price.append(
            ast.literal_eval(stock_dict[key][close])
        )

    
    closing_price = closing_price[::-1]

    price_uptodate = closing_price[-1]

    L = len(closing_price)

    # 52-weeks Highs and Lows
    # 
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
    # print(name, _52_week_high, _52_week_low)
    averages = [50, 150, 200]
    rolling_averages = {}
    for X in averages:
        avg = []
        for idx, ele in enumerate(closing_price):
            if idx < L - One_Year_Ish:
                continue
            x_ = sum(closing_price[idx - X : idx]) / X
            avg.append(x_)
        rolling_averages[X] = avg[-1]


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
    if score >= 6:
        results.append([
            name,score
        ])

print(f"{len(results)} tickers past out of {len(relevant_data)} total files.")
# FGH = np.asarray([
#     four_out_of_seven,five_out_of_seven,six_out_of_seven,seven_out_of_seven
# ])
# np.savetxt('test.txt', FGH)

f = open(out_file,"a+")
for item in results:
    f.write(f"{item[0]}\n")
f.close()