import numpy as np
import requests
import time
import pandas as pd
import sys,os
from io import BytesIO

test = open('LSE.txt', 'r')
elements = test.readlines()[1:]
equity_stocks = []
for str in elements:
    tab_loc = str.index("\t")
    if tab_loc <= 4:
        equity_stocks.append(
            str[0:tab_loc]
        )

L_All = len(equity_stocks)

today = int(time.time())
one_year_hence = today - 3600*24*365

success = []
from progress.bar import Bar

def link(stock_name, start_date, end_date):
    return(
        "https://query2.finance.yahoo.com/v7/finance/download/%s.L?period1=%s&period2=%s&interval=1d&events=history"%(stock_name, start_date, end_date)
    )

# https://query1.finance.yahoo.com/v7/finance/download/CAD.L?period1=1568495506&period2=1600117906&interval=1d&events=history


report_me = 'report.txt'
if os.path.exists(report_me):
    os.remove(report_me)

# removal = 'removed.txt'
# if os.path.exists(removal):
#     os.remove(removal)
# if os.path.exists('faulty_link.txt'):
#     os.remove('faulty_link.txt')
# exit()

bar = Bar('Processing stock data:', max = len(equity_stocks), suffix = '%(percent).1f%%')
downloaded = 0
updated = 0
for idx,x_ in enumerate(equity_stocks):

    write_me = '%s:\n'%x_
    filepath = 'All_Stocks/%s.csv'%x_
    temp_fp  = 'All_Stocks/temp.csv'
    if os.path.exists(filepath):
        write_me += '    >CSV Exists\n'
        existing_csv = pd.read_csv(filepath, sep=',')#, index_col=0)
        if len(existing_csv.columns) > 7:
            existing_csv = pd.read_csv(filepath, index_col=0, sep=',')
        
        last_updated = existing_csv['Date'].iloc[-1]
        l = link(x_, one_year_hence, today)
        r = requests.get(l, allow_redirects = True)
        if r.ok:
            pass
        else:
            write_me += '    >Link no longer working\n'
            # os.remove(filepath)
            continue
        write_me += '    >Link working....'
        open(temp_fp,'wb').write(r.content)
        new_csv = pd.read_csv(temp_fp, sep=',')
        idx = new_csv.set_index('Date').index.get_loc(last_updated)
        subframe = new_csv[idx+1::]
        existing_csv = existing_csv.append(
            subframe, ignore_index=True
        )
        existing_csv.to_csv(filepath)
        write_me += 'CSV updated\n'
        updated += 1

    else:
        write_me += '    >CSV not present\n'
        l = link(x_, one_year_hence, today)

        r = requests.get(l, allow_redirects = True)
        # print(r.content)
        if not r.status_code == 401 and r.ok:
            # print(x_, 'link ok')
            # sys.stdout.write('\r%s, %s'%(idx, x_))
            # sys.stdout.flush()
            # time.sleep(0.5)
            cr = BytesIO(r.content)
            df = pd.read_csv(cr, sep=',')
            L = len(df)
            write_me += '    >Link okay and sizeable dataset\n'
            c = df["Open"].isnull().sum()
            if pd.isnull(df.iloc[-1]["Open"]) or (c/L > 0.05) or L < 100:
                write_me += '    >Rejected: too many null fields.\n'
                pass
            else:
                write_me += '    >Accepted: CSV created.\n'
                df.to_csv(filepath)
                downloaded += 1
        else:
            write_me += '    >Link faulty\n'
        
    if os.path.exists(temp_fp):
        os.remove(temp_fp)
    write_me+= '\n'
    g = open(report_me,"a+")
    g.write(write_me)
    g.close()
    bar.next()
bar.finish()
print('\n%s equity tickers tested; %s updated and %s downloaded.'%(L_All, updated, downloaded))