#  GRAPH CREATION FOR MARKOWITZ.PY

# graph requirements
import mpld3
from mpld3 import plugins
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
from operations import mprint
import plugs


def pct_format(x):
    if x <= 0:
        return '{:.0f}%'.format(x)
    else:
        return '+{:.0f}%'.format(x)

def plt_to_img(plt, name="ghoozie",dpi=100):
    importlib.reload(matplotlib)
    s = io.BytesIO()

    html = mpld3.fig_to_html(plt.gcf())
    plt.savefig("/app/plts/{}.pdf".format(name), format='pdf', facecolor="white", bbox_inches='tight')
    # plt.savefig("/app/plts/{}.png".format(name), format='png', dpi=dpi, facecolor="white", bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return html
    #return "data:image/png;base64,%s" % s


def calc_norm(mu,sigma,z):
    d = .02
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


def bell(mu=1.10,sigma=.071,title='',color='b',legend=''):
    mu = mu*100
    sigma = sigma*100

    # build the plot

    fig, ax = plt.subplots(figsize=(9,6))
    bigger_top = plt.ylim()[1]*1.2
    plt.ylim(bottom=0.0,top=bigger_top)

    # draw bell
    ax, x, y = draw_bell(ax, mu, sigma, color=color)

    ax.set_xlim([mu-4*sigma,mu+4*sigma])
    ax.set_xlabel('% Return',fontsize=16)
    ax.set_ylabel('Probability Distribution',fontsize=16)
    ax.set_yticklabels([])

    plt.xticks(np.arange(min(x), max(x)+1, sigma),fontsize=16)
    plt.gca().set_xticklabels([pct_format(x) for x in plt.gca().get_xticks()])

    ax.set_title('Bell Curve Of Returns',fontsize=16)
    ax.legend([legend], loc='upper left')

    return plt_to_img(plt, "bell"+title)


def bell_compare(mu=110, mu2=100, sigma=7.10, sigma2=8):
    mu, mu2 = mu*100, mu2*100
    sigma, sigma2 = sigma*100, sigma2*100

    # build the plot
    fig, ax = plt.subplots(figsize=(9,6))
    bigger_top = plt.ylim()[1]*1.2
    plt.ylim(bottom=0.0,top=bigger_top)

    # draw bells
    ax, x, y = draw_bell(ax, mu2, sigma2, zorder=1, color='b', alpha=.1)
    ax, x, y = draw_bell(ax, mu, sigma, zorder=2, color='mediumSeaGreen', alpha=.3)

    ax.set_xlim([mu-4*sigma,mu+4*sigma])
    ax.set_xlabel('% Return',fontsize=16)
    ax.set_ylabel('Probability Distribution',fontsize=16)
    ax.set_yticklabels([])

    plt.xticks(np.arange(min(x), max(x)+1, sigma),fontsize=16)
    plt.gca().set_xticklabels([pct_format(x) for x in plt.gca().get_xticks()])

    ax.set_title('Bell Curve Of Returns',fontsize=16)

    #legend
    ax.legend(['Current', 'Recommended'], loc='upper left')

    return plt_to_img(plt, "bellcompare",300)


def draw_line(plt, line_data, color="black", zorder=1):
    year = line_data.keys()
    ret = [line_data[x][0] for x in line_data]

    year = [int(date.today().year) + y for y in year]
    plt.plot(year, ret, color=color, marker='o', zorder=zorder)

    #added [1:] indexing so line graphs start at accurate wealth number (i donut know why it was off before)
    plt.gca().set_yticklabels(["$" + '{:,}'.format(int(x)) for x in plt.gca().get_yticks()[1:]])


def line(line_data, title=0):
    draw_line(plt, line_data)
    if title == 1:
        ystring = ' Year'
    else:
        ystring = ' Years'

    plt.title('Expected Returns For ' + str(title) + ystring, fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True, color='lightgray')
    plt.rc('grid', color='lightgray')

    return plt_to_img(plt, "line" + str(title))


def line_compare(rline_data, bline_data, title=1):
    draw_line(plt, rline_data, color="red", zorder=2)
    draw_line(plt, bline_data, color="blue", zorder=1)
    if title == 1:
        ystring = ' Year'
    else:
        ystring = ' Years'

    plt.title('Expected Returns For ' + str(title) + ystring, fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True)
    plt.legend(['Recommended','Current'], loc='upper left')

    return plt_to_img(plt, "line" + str(title),300)


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

    fig1, ax1 = plt.subplots(figsize=(9,6))

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
    ax1.pie(sizes, labels=tickers, explode=explode, colors='w', autopct='%1.1f%%', shadow=False, startangle=180,
                    wedgeprops={"edgecolor":"0", 'linewidth': 0.65, 'antialiased': True},
                    textprops={'fontsize': 14})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt_to_img(plt, title)


def noise(daily_data, labels):
    plt.figure(figsize=(10,6))
    plt.plot(daily_data.T, alpha=.4, )

    plt.gca().set_yticklabels([pct_format(x * 100 - 100) for x in plt.gca().get_yticks()])
    plt.xlabel('Time (Date)')
    plt.ylabel('Price (%)')
    plt.title('Daily Performance Of Chosen Assets');
    plt.legend(labels, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()

    return plt_to_img(plt, "noise",300)


def d3dymo(plt, points, labels):
    tooltip = plugs.customHover(points[0], labels=labels)
    # tooltip = plugs.dHover()
    plugins.connect(plt.gcf(), tooltip)


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

    # plot trans ribs
    plt.ylabel('Return (Percentage)')
    plt.xlabel('Risk (Standard Deviation)')
    riskys = [r*s for r in ribs['risk']]
    retys = [r*s for r in ribs['ret']]
    points = plt.plot(riskys, retys, 'w-o',markersize=5*ms,alpha = 0,zorder=2)
    labels = ['Risk: ' + str(riskys[i])[:4] + ', Return: ' + str(retys[i])[:4] for i, r in enumerate(ribs['ret'])]
    d3dymo(plt, points, labels)

    # plot ribs
    plt.ylabel('Return (Percentage)')
    plt.xlabel('Risk (Standard Deviation)')
    riskys = [r*s for r in ribs['risk']]
    retys = [r*s for r in ribs['ret']]
    points = plt.plot(riskys, retys, 'y-o',markersize=ms)
    

    # plot slider-selected recommended portfolio
    plt.plot(red['risk'] * s,red['ret'] * s,'o',color='red',zorder=3,markersize=ms*2.2)
    # labels = ["Risk: " + str(red['risk'])[:4] + ", Return:"]

    # plot original portfolio
    plt.plot(blue['risk'] * s,blue['ret'] * s,'o',color='blue',zorder=4,markersize=ms*2.2)

    # title the graph
    plt.title('Expected Return and Risk Of Portfolios')


    return plt_to_img(plt, "frontier",300)