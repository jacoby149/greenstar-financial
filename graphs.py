#  GRAPH CREATION FOR MARKOWITZ.PY

# graph requirements
import io
import base64
import importlib
import numpy as np
import pandas as pd
from scipy.stats import norm

#matplotlib necessary imports
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# in-house
import operations as ops




def plt_to_img(plt, name="ghoozie"):
    importlib.reload(matplotlib)
    s = io.BytesIO()

    plt.savefig(s, format='png', dpi=100, facecolor="white", bbox_inches='tight')
    plt.savefig("/app/plts/{}.png".format(name), format='png', dpi=100, facecolor="white", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s" % s


def calc_norm(mu,sigma,z):
    d = .001
    x = np.arange(mu-z*sigma,mu+z*sigma,d*sigma)
    y = norm.pdf(x,mu,sigma)
    return x, y


def normal(mu=110,sigma=7.10):
    x_t,y_t = calc_norm(mu,sigma,1)
    x,y = calc_norm(mu,sigma,2)
    x_all,y_all = calc_norm(mu,sigma,10)

    # build the plot
    fig, ax = plt.subplots(figsize=(9,6))

    #adjust the graph so the x axis is zero
    ax.spines['bottom'].set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    #plt.style.use('fivethirtyeight')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    #revenue marks
    ax.plot(x_all,y_all)

    ax.fill_between(x_t,y_t,0, alpha=0.3, color='g')
    ax.fill_between(x,y,0, alpha=0.3, color='b')
    ax.fill_between(x_all,y_all,0, alpha=0.1)

    ax.set_xlim([mu-4*sigma,mu+4*sigma])

    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    ax.set_ylabel('Probability Distribution')

    ax.set_yticklabels([])
    plt.xticks(np.arange(min(x), max(x)+1, sigma))

    ax.set_title('Bell Curve Of Returns')

    return plt_to_img(plt, "bell")


def pie(sizes=None, tickers=None, title='pie_default'):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    if tickers is None:
        tickers = 'FB', 'MSFT', 'AMZN', 'GOOG'

    if sizes is None:
        sizes = ops.rand_weights(4)

    explode = [0 for t in tickers]
    explode[0] = .1

    # max_ticker = max(tickers.keys(), key=(lambda k: tickers[k]))   <-- Explode largest slice of pie

    print("sizes: ", sizes)
    print("tickers: ", tickers)
    print("explode: ", explode)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=tickers, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt_to_img(plt, title)


def line(years=''):
    Data = {'Year': [2020,2021,2022,2023,2024,2025,2026],
            'Return': [100,105,111,118,127,137,148], }

    df = pd.DataFrame(Data,columns=['Year','Return'])

    plt.plot(df['Year'], df['Return'], color='black', marker='o')
    plt.title('Expected Returns For 7 Years', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True)

    return plt_to_img(plt, "line" + str(years))


def noise(daily_data, labels):
    plt.plot(daily_data.T, alpha=.4);

    def pct_format(x):
        if x <= 0:
            return '{:.0f}%'.format(x)
        else:
            return '+{:.0f}%'.format(x)

    plt.gca().set_yticklabels([pct_format(x * 100 - 100) for x in plt.gca().get_yticks()])
    plt.xlabel('Time (Date)')
    plt.ylabel('Price (%)')
    plt.title('Daily Performance Of Chosen Assets');
    plt.legend(labels, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()

    return plt_to_img(plt, "noise")


def frontier(red, blue, wheat, ribs):
    # Percentage plot rather than decimal plot
    s = 100
    ms = 2

    # Format axes
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    # Legend
    legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
                       Line2D([0], [0], marker='o', color='w', label='Scatter',
                              markerfacecolor='g', markersize=15),
                       Patch(facecolor='orange', edgecolor='r',
                             label='Color Patch')]
    ax.legend(handles=legend_elements)#, loc='center')

    #plot random portfolios
    plt.plot([r*s for r in wheat['risk']], [r*s for r in wheat['ret']], 'o',color="wheat",markersize=ms)

    # plot optimal portfolios
    plt.ylabel('Return (Percentage)')
    plt.xlabel('Risk (Standard Deviation)')
    plt.plot([r*s for r in ribs['risk']], [r*s for r in ribs['ret']], 'y-o',markersize=ms)

    # plot slider-selected recommended portfolio
    plt.plot(red['risk'],red['ret'],'o',color='red',zorder=2,markersize=ms*2)

    # plot original portfolio
    plt.plot(blue['risk'] * s,blue['ret'] * s,'o',color='blue',zorder=3,markersize=ms*2)

    # title the graph
    plt.title('Expected Return and Risk Of Portfolios')

    return plt_to_img(plt, "frontier")