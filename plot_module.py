import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import numpy as np


def plot_graph(name, dates, closing_price, volume, rolling_averages):
    averages = [100, 150, 200]
    L = len(closing_price)
    mpl.style.use('seaborn')
    mpl.rcParams['mathtext.fontset'] = 'stix'
    mpl.rcParams['font.family'] = 'STIXGeneral'
    mpl.rcParams['axes.linewidth'] = 1.2

    nticks = 12
    ticks = np.linspace(0, L - 1, nticks, dtype = int)

    labels = []
    for str in dates[ticks]:
        frmt = datetime.strptime(str,'%Y-%m-%d')
        newfrmt = frmt.strftime('%d %b %y')
        labels.append(newfrmt)

    w = 15
    h = 7
    d = 70

    plt.figure(figsize=(w, h), dpi=d)

    f1 = plt.subplot(2,1,1)
    plt.plot(dates, closing_price, color = 'grey')
    for idx, X in enumerate(averages):
        plt.plot(dates, rolling_averages[idx], label = '%s-day avg'%X)
    plt.setp(f1.get_xticklabels(), visible=False)#input_csv['Date'][ticks], labels, rotation = 30, fontsize = 15)

    plt.legend(fontsize = 18)
    plt.ylabel('Price', fontsize = 18)
    plt.grid(True)

    f2 = plt.subplot(2,1,2, sharex = f1)
    plt.plot(dates, volume)
    plt.xticks(dates[ticks], labels, rotation = 30, fontsize = 15)
    plt.tick_params(direction='out', length=6, width=2, grid_alpha=0.5)
    plt.ylabel('Volume', fontsize = 18)
    plt.tight_layout()
    plt.savefig(name + '.pdf', bbox_inches = 'tight')