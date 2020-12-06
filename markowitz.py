#adapted quantopian markowitz code

#graph requirements
import io
import base64
#import numpy as np
#import matplotlib.pyplot as plt
from scipy.stats import norm

from urllib.request import urlopen

#markowitz requirements.
import numpy as np
from numpy import array
from numpy import isnan

import importlib

#matplotlib necessary imports
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


import cvxopt as opt
from cvxopt import blas, solvers
solvers.options['show_progress'] = False
import copy

# backtesting requirements
import matplotlib.pyplot as plt
import pandas as pd
import os

import yfinance as yf
import pandas_datareader as pdr



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


def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)


def pie(sizes=rand_weights(4), tickers=None, num=''):
    import matplotlib.pyplot as plt

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    if tickers is None:
        tickers = 'FB', 'MSFT', 'AMZN', 'GOOG'
    explode = [0 for t in tickers]
    explode[0] = .1

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=tickers, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt_to_img(plt, "pie" + num)

def line(years=''):
    Data = {'Year': [2020,2021,2022,2023,2024,2025,2026],
            'Return': [100,105,111,118,127,137,148]
        }
    
    df = pd.DataFrame(Data,columns=['Year','Return'])
    
    plt.plot(df['Year'], df['Return'], color='black', marker='o')
    plt.title('Expected Returns For 7 Years', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.grid(True)
    return plt_to_img(plt, "line" + str(years))


def optimal_portfolio(daily_data):
    n = len(daily_data)
    daily_data = np.asmatrix(daily_data)

    N = 500            # Bigger N, bigger upper range, less lower range and less control. Smaller N, smaller range more control, more lower values
    if 0 <= n <= 7:
        power = n + 1
    else:
        power = 8.0
    #the first 20 porfolios are
    mus = [10**(power * t/N - 1.0) for t in range(0,200)]
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(daily_data))
    pbar = opt.matrix(np.mean(daily_data, axis=1))

    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER using linear algebra solving
    returns = [blas.dot(pbar, p) for p in portfolios]
    risks = [np.sqrt(blas.dot(p, S*p)) for p in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    
    #Calculates "optimal" portfolio, but better to let customer choose
    #m1 = np.polyfit(returns, risks, 2)
    #x1 = np.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    #wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    #return np.asarray(wt), returns, risks
    
    return portfolios,returns,risks


#number of assets - number of stocks
#number of observations - number of days
#g - rate of average daily growth in positions 
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


# from morningstar.morningstar_client import MorningstarClient
def asset_classes(tickers):
    from datetime import date,timedelta
    print("TICKERS :", tickers, flush=True)
    end_date = date.today()
    d = timedelta(days=1800)
    start_date = end_date - d

    # client = MorningstarClient()
    # mstar = client.get_instrument_prices(instrument='^SP400', start_date=str(start_date), end_date=str(end_date))

    labels = " ".join(tickers)
    yahoo = yf.download(labels, start=str(start_date), end=str(end_date))['Adj Close']
    yahoo.to_csv('tickers.csv')
    # print("head : ", yahoo.head(), flush=True)
    # print("dates: ", start_date, " ... ", end_date, flush=True)
    # print("YAHOO :", yahoo.values, flush=True)
    # print('ytype :', type(yahoo), flush=True)
    # print(flush=True) relaod

    yahoo = yahoo.to_numpy()

    yahoo = np.reshape(yahoo, (yahoo.shape[0], -1))
    print("yahoo shape : ", yahoo.shape, flush=True)

    #  Averages each ticker based on the value from first day listed
    yahoo = yahoo / yahoo[0]

    findnans = isnan(yahoo)
    yahoo[findnans] = 1

    yahoo = yahoo.T
    print("T shape: ", yahoo.shape, flush=True)

    return yahoo, labels


def random_assets(n_assets=4, n_obs=1000, g=1.00026):
    #TODO add g in here
    np.random.seed(123)
    # Turn off progress printing 
    solvers.options['show_progress'] = False
    # Assume that we have 4 assets, each with a return series of length 1000. We can use `numpy.random.randn` to sample returns from a normal distribution.
    # In[2]:

    daily_data = np.random.randn(n_assets, n_obs)/4 + 1
    daily_data[daily_data < 0] = 0
    gain_vector = [g**n for n in range(n_obs)]
    daily_data = daily_data*gain_vector
    return daily_data


def neat(portfolios):
    def n(p):
        p = array(p)
        p = np.round(p,2)
        p = p.tolist()
        return p
    portfolios = [n(p) for p in portfolios]
    return portfolios


def portfolio_performance(daily_data, weights=None):
    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''
    if (weights == None): weights = rand_weights(daily_data.shape[0])
    p = np.asmatrix(np.mean(daily_data, axis=1))
    w = np.asmatrix(weights)
    C = np.asmatrix(np.cov(daily_data))

    #calculates earning and
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    # print("randweight shape: ", w.shape)
    # print("p.T shape: ", p.T.shape)

    # This recursion reduces outliers to keep plots pretty
    # re-draws a random portfolio
    # if sigma > 2:
    #    return portfolio_performance(daily_data)
    return mu, sigma


def customer_port_weights(captable):
    if captable is None:
        return [.2, .3, .2, .3]

    allocations = [int(captable[x]) for x in captable if "X".casefold() not in captable[x].casefold() and captable[x] != '']
    allocations = [a / sum(allocations) for a in allocations]
    print("allocations: ", allocations)
    return allocations



import pickle
import matplotlib.ticker as mtick

def markowitz_run(daily_data=random_assets(), tickers=None, captable=None, risk_level=50):
    if tickers is not None:
        daily_data, labels = asset_classes(tickers)
        labels = labels.split(" ")
        labels.sort()
    else:
        labels = ["F", "A", "N", "g"]

    images = []

    plt.plot(daily_data.T, alpha=.4);

    def pct_format(x):
        if x <= 0:
            return '{:.0f}%'.format(x)
        else:
            return '+{:.0f}%'.format(x)

    plt.gca().set_yticklabels([pct_format(x*100 - 100) for x in plt.gca().get_yticks()])

    plt.xlabel('Time (Date)')
    plt.ylabel('Price (%)')
    plt.title('Daily Performance Of Chosen Assets');


    plt.legend(labels, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()

    images.append(plt_to_img(plt, "noise"))

    n_portfolios = 500
    means, stds = np.column_stack([
        portfolio_performance(daily_data) 
        for _ in range(n_portfolios)
    ])
    
    portfolios, returns, risks = optimal_portfolio(daily_data)
    #2d list instead of numpy array

    portfolios.reverse()
    returns.reverse()
    risks.reverse()

    s = 100 #percentage plot rather than decimal plot
    ms = 2
    #format the figure axes
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    #custom legend
    legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
                   Line2D([0], [0], marker='o', color='w', label='Scatter',
                          markerfacecolor='g', markersize=15),
                   Patch(facecolor='orange', edgecolor='r',
                         label='Color Patch')]
    ax.legend(handles=legend_elements)#, loc='center')

    #plot the random portfolios
    plt.plot([r*s for r in stds], [r*s for r in means], 'o',color="wheat",markersize=ms)

    #plot the optimal portfolios
    plt.ylabel('Return (Percentage)')
    plt.xlabel('Risk (Standard Deviation)')
    plt.plot([r*s for r in risks], [r*s for r in returns], 'y-o',markersize=ms)
    
    #plot the slider selected portfolio
    risk_new, ret_new = [risks[risk_level]*s], [returns[risk_level]*s]
    plt.plot(risk_new,ret_new,'o',color='red',zorder=2,markersize=ms)

    #plot the customer original portfolio
    weights = customer_port_weights(captable)
    ret_curr, risk_curr = portfolio_performance(daily_data,weights=weights)
    plt.plot(risk_curr*s,ret_curr*s,'o',color='blue',zorder=3,markersize=ms)

    ###   GENERATE LATEX INPUTS FOR FRONTIER PAGE
    def stringit(v):
        if v == 0:
            v = "$\pm$ " + str(v)
        elif v > 0:
            v = "+ " + str(v)
        else:
            v = str(v)
        return v

    ret_curr = ret_curr.tolist()
    risk_curr = risk_curr.tolist()

    ret_curr = ret_curr[0][0]
    risk_curr = risk_curr[0][0]
    ret_new = ret_new[0]
    risk_new = round(risk_new[0], 2)

    risk_change = round((risk_new - risk_curr), 2)

    risk_change = stringit(risk_change)
    ret_improve = ret_new - ret_curr

    ret_new = stringit(round((ret_new - 100), 1))
    ret_improve = stringit(round((ret_improve - 100), 1))


    port_vars = {"ret_curr": ret_curr, "risk_curr": risk_curr,
                 "ret_new": ret_new, "risk_new": risk_new,
                 "risk_change": risk_change, "ret_improve": ret_improve}

    with open("port_vars.pickle", 'wb') as port_pickle:
        pickle.dump(port_vars, port_pickle)

    plt.title('Expected Return and Risk Of Portfolios')
    images.append(plt_to_img(plt, "frontier"))
    images.append(pie(weights, tickers))

    portfolios = neat(portfolios)

    return images,portfolios,returns,risks


