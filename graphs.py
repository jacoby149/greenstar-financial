#  GRAPH CREATION FOR MARKOWITZ.PY

# graph requirements
import io
import math
import base64
import importlib
import numpy as np
import pandas as pd
from datetime import date
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


def draw_bell(ax, mu=110,sigma=7.10, zorder=1, color='g', alpha=0.3):
    x_t, y_t = calc_norm(mu,sigma,1)
    x, y = calc_norm(mu,sigma,2)
    x_all, y_all = calc_norm(mu,sigma,10)
    y, y_t, y_all = y / max(y), y_t / max(y_t), y_all / max(y_all)

    #revenue marks
    ax.plot(x_all, y_all, zorder=zorder, alpha=0.7, color=color)
    ax.fill_between(x_t, y_t, 0, alpha=alpha, color=color, zorder=zorder)
    ax.fill_between(x, y, 0, alpha=alpha, color=color, zorder=zorder)
    ax.fill_between(x_all, y_all, 0, alpha=alpha/3, zorder=zorder)

    return ax, x, y


def bell(mu=1.10,sigma=.071):
    mu = mu*100
    sigma = sigma*100

    # build the plot
    fig, ax = plt.subplots(figsize=(9,6))

    # draw bell
    ax, x, y = draw_bell(ax, mu, sigma, color='r')

    # format for percent
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    # adjust the graph so the x axis is zero
    ax.spines['bottom'].set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xlim([mu-4*sigma,mu+4*sigma])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    ax.set_ylabel('Probability Distribution')
    ax.set_yticklabels([])

    plt.xticks(np.arange(min(x), max(x)+1, sigma))
    ax.set_title('Bell Curve Of Returns')

    return plt_to_img(plt, "bell")


def bell_compare(mu=110, mu2=100, sigma=7.10, sigma2=8):
    mu, mu2 = mu*100, mu2*100
    sigma, sigma2 = sigma*100, sigma2*100

    # build the plot
    fig, ax = plt.subplots(figsize=(9,6))

    # draw bells
    ax, x, y = draw_bell(ax, mu, sigma, zorder=2, color='mediumSeaGreen', alpha=.3)
    plt.xticks(np.arange(min(x), max(x)+1, sigma))
    ax, x, y = draw_bell(ax, mu2, sigma2, zorder=1, color='b', alpha=.1)

    # format for percent
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    #adjust the graph so the x axis is zero
    ax.spines['bottom'].set_position('zero')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xlim([mu-4*sigma,mu+4*sigma])
    ax.set_xlabel('# of Standard Deviations Outside the Mean')
    ax.set_ylabel('Probability Distribution')
    ax.set_yticklabels([])

    ax.set_title('Bell Curve Of Returns')

    return plt_to_img(plt, "bellcompare")


def draw_line(plt, line_data, color="black", zorder=1):
    year, ret = line_data.keys(), line_data.values()
    year = [y + int(str(date.today())[:4]) for y in year]
    plt.plot(year, ret, color=color, marker='o', zorder=zorder)


def line(line_data, title=0):
    draw_line(plt, line_data)
    plt.title('Expected Returns For ' + str(title) + ' Years', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True)

    return plt_to_img(plt, "line" + str(title))


def line_compare(rline_data, bline_data, title=1):
    draw_line(plt, bline_data, color="blue", zorder=1)
    draw_line(plt, rline_data, color="red", zorder=2)
    plt.title('Expected Returns For ' + str(title) + ' Years', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True)

    return plt_to_img(plt, "line" + str(title))


def pie(pie_data, title='pie_default'):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    if pie_data is None:
        tickers = 'FB', 'MSFT', 'AMZN', 'GOOG'
        sizes = ops.rand_weights(4)
    else:
        tickers, sizes = pie_data.keys(), pie_data.values()

    explode = [0 for t in tickers]
    explode[0] = .1

    # max_ticker = max(tickers.keys(), key=(lambda k: tickers[k]))   <-- Explode largest slice of pie

    fig1, ax1 = plt.subplots()

    def hexy(x):
        y = hex(x)[2:]
        if len(y) == 1:
            return "0" + y
        elif len(y) > 2:
            return "ff"
        else:
            return y

    gcolors = ["#" + hexy(255) + hexy(255) + hexy(255) for x in range(100,255,20)]

    colors = ['cornflowerblue', 'limegreen', 'orangered', 'gold', 'm', 'c', 'k']
    ax1.pie(sizes, labels=tickers, explode=explode, colors=colors, autopct='%1.1f%%', shadow=False, startangle=180,
                    wedgeprops={"edgecolor":"0", 'linewidth': 0.65, 'antialiased': True})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt_to_img(plt, title)


def noise(daily_data, labels):
    plt.figure(figsize=(10,6))
    plt.plot(daily_data.T, alpha=.4, )

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
    fig, ax = plt.subplots(figsize=(9,6))

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    # Legend
    legend_elements = [Line2D([0], [0], marker='o', lw=0, color='b', label='Current Strategy', markersize=5),
                       Line2D([0], [0], marker='o', lw=0, color='r', label='Recommended Strategy', markersize=5),
                       Line2D([0], [0], marker='o', lw=0, color='wheat', label='Generic Portfolios', markersize=5),
                       Line2D([0], [0], color='y', lw=2.0, label='Optimal Portfolios')]

    ax.legend(handles=legend_elements)

    #plot random portfolios
    plt.plot([r*s for r in wheat['risk']], [r*s for r in wheat['ret']], 'o',color="wheat",markersize=ms)

    # plot optimal portfolios
    plt.ylabel('Return (Percentage)')
    plt.xlabel('Risk (Standard Deviation)')
    plt.plot([r*s for r in ribs['risk']], [r*s for r in ribs['ret']], 'y-o',markersize=ms)

    # plot slider-selected recommended portfolio
    plt.plot(red['risk'] * s,red['ret'] * s,'o',color='red',zorder=2,markersize=ms*1.6)

    # plot original portfolio
    plt.plot(blue['risk'] * s,blue['ret'] * s,'o',color='blue',zorder=3,markersize=ms*1.6)

    # title the graph
    plt.title('Expected Return and Risk Of Portfolios')

    return plt_to_img(plt, "frontier")