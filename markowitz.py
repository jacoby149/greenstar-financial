# adapted quantopian markowitz code


# in-house
import graphs
import operations as ops
from operations import mprint
import report

from urllib.request import urlopen

#markowitz requirements.
import numpy as np
from numpy import array
from numpy import isnan

from datetime import date,timedelta

import pickle
import pandas as pd

import cvxopt as opt
from cvxopt import blas, solvers
import copy

# backtesting requirements
import os

# data collection
import yfinance as yf
import pandas_datareader as pdr


# Turns off prints for convex optimizer
solvers.options['show_progress'] = False



#################################
#######  DATA FUNCTIONS  ########
#################################

def yahoo_assets(tickers):
    # mprint("TICKERS",tickers)
    end_date = date.today()
    d = timedelta(days=1800)
    start_date = end_date - d

    tickers = " ".join(tickers)
    filename = "csv/yfinance" + str(end_date) + tickers + ".csv"

    print("collecting daily data:")
    if os.path.exists(filename):
        print(filename + " exists\n")
        yahoo = pd.read_csv(filename, index_col="Date")
    else:
        print("downloading data from yahoo\n")
        yahoo = yf.download(tickers, start=str(start_date), end=str(end_date))['Adj Close']
        yahoo.to_csv(filename)

    # mprint("yahoo data",yahoo.values)
    # mprint("yahoo shape",yahoo.shape)
    # mprint("yahoo type",type(yahoo))          yahoo downloads as a nice looking pandas dataframe


    def clean(yahoo):
        yahoo = yahoo.to_numpy()
        yahoo = np.reshape(yahoo, (yahoo.shape[0], -1))
        yahoo = yahoo / yahoo[0]

        # normalizes nan values
        findnans = isnan(yahoo)
        yahoo[findnans] = 1

        yahoo = yahoo.T
        # mprint("T shape",yahoo.shape)
        return yahoo

    yahoo = clean(yahoo)
    # mprint('yahoo',yahoo)                     yahoo exports as a numpy matrix

    return yahoo


def random_assets(n_assets=4, n_obs=1000, g=1.00026):
    np.random.seed(123)

    daily_data = np.random.randn(n_assets, n_obs)/4 + 1
    daily_data[daily_data < 0] = 0
    gain_vector = [g**n for n in range(n_obs)]
    daily_data = daily_data*gain_vector

    return daily_data



#################################
#######  PORTFOLIO CALC  ########
#################################

def optimal_portfolio(daily_data):
    n = len(daily_data)
    daily_data = np.asmatrix(daily_data)
    mus = ops.get_mus(N=500, t=200, n=n)
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(daily_data))
    pbar = opt.matrix(np.mean(daily_data, axis=1))

    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    
    # Calculate rib frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus]

    # Calculate risk and return for frontier using linear algebra solving
    returns = [blas.dot(pbar, p) for p in portfolios]
    risks = [np.sqrt(blas.dot(p, S*p)) for p in portfolios]

    # risk slider is inverted without these
    portfolios.reverse()
    returns.reverse()
    risks.reverse()

    # mprint('returns',returns)
    # mprint('risks',risks)

    return portfolios,returns,risks


def get_rand_portfolio(daily_data):
    # Returns the mean and standard deviation of returns for a random portfolio
    return ops.portfolio_performance(daily_data, ops.rand_weights(daily_data.shape[0]))


def customer_port_weights(leanbook):
    captable = dict(zip(leanbook.ticker,leanbook.allocation))

    allocations = [int(captable[x]) for x in captable]
    allocations = [a / sum(allocations) for a in allocations]

    # mprint("allocations",allocations)
    return allocations


def old_weights(leanbook):
    captable = dict(zip)

    allocations = [(captable[x], x) for x in captable]
    allocations = sorted(allocations, key=lambda x: x[1])
    allocations = [a[0] for a in allocations]
    for i, item in enumerate(allocations):
        if 'X' in item:
            item = item[:-1]
        allocations[i] = int(item)

    allocations = [a / sum(allocations) for a in allocations]

    return allocations



#################################
#######  MARKOWITZ RUN   ########
#################################

def dataframe_structures(book):
    # get structures for future strategy (red)
    redbook = book.loc[~book['allocation'].str.startswith('-')]  # & (~book['allocation'].isin([str(val) + 'X' for val in range(max(int(book['allocation'])))]))]
    rtickers = redbook['ticker'].tolist()

    mprint('future book',redbook)
    mprint('future tickers',rtickers)

    # get structures for current strategy (blue)
    bluebook = book.loc[(book['allocation'] != '-') & (book['allocation'] != '0')]
    btickers = bluebook['ticker'].tolist()

    mprint('old book',bluebook)
    mprint('old tickers',btickers)

    # get structures for yahoo's daily_data (yahoo)
    ybook = book.loc[book['allocation'] != '-']
    ytickers = ybook['ticker'].tolist()

    mprint('yahoo book',ybook)
    mprint('yahoo tickers',ytickers)

    return rtickers, redbook, btickers, bluebook, ytickers, ybook



def markowitz_run(book, info):
    images = []
    rtickers, redbook, btickers, bluebook, ytickers, ybook = dataframe_structures(book)


    daily_data = yahoo_assets(ytickers)

    def get_frontier_data():
        risk_level = int(info['risk'])

        # get wheats data (frontier)
        means, stds = np.column_stack([get_rand_portfolio(daily_data) for _ in range(500) ])

        # get ribs data (frontier)
        portfolios, returns, risks = optimal_portfolio(daily_data)

        # get red data (frontier)
        ret_new, risk_new = returns[risk_level], risks[risk_level]

        # get blue data (frontier)
        allocations = customer_port_weights(leanbook)
        ret_curr, risk_curr = ops.portfolio_performance(daily_data,weights=allocations)

        # pack dictionary for quick unload
        red = {"ret": ret_new, "risk": risk_new}
        blue = {"ret": ret_curr, "risk": risk_curr, "weights": weights}
        wheat = {"ret": means, "risk": stds}
        ribs = {"ret": returns, "risk": risks, 'port': portfolios}

        return red, blue, wheat, ribs

    red, blue, wheat, ribs = get_frontier_data()


    # remapping to relevant assets
    old_assets = [asset_map[ticker] for ticker in btickers]
    assets = [asset_map[ticker] for ticker in tickers]

    # get pie data
    ol_pie = dict(zip(old_assets, old_weights(leanbook)))
    fpd = dict(zip(assets, ribs['port'][risk_level]))
    new_pie = {asset: fpd[asset] for asset in fpd if fpd[asset] > 0.0005}


    # make frontier graph
    images.append(graphs.frontier(red, blue, wheat, ribs))


    # make pie graphs
    images.append(graphs.pie(new_pie, 'piefuture'))
    images.append(graphs.pie(ol_pie, 'pie'))


    # Make noise graph
    images.append(graphs.noise(daily_data, assets))


    # Make line graphs
    rline_data = ops.montecarlo(mu=red['ret'], std=red['risk'], term=1, trials=1000, starting_wealth=sum([int(x) for x in captable.values()]))
    bline_data = ops.montecarlo(mu=blue['ret'], std=blue['risk'], term=1, trials=1000, starting_wealth=sum([int(x) for x in captable.values()]))
    images.append(graphs.line_compare(rline_data, bline_data))

    rline_data = ops.montecarlo(mu=red['ret'], std=red['risk'], term=7, trials=1000, starting_wealth=sum([int(x) for x in captable.values()]))
    bline_data = ops.montecarlo(mu=blue['ret'], std=blue['risk'], term=7, trials=1000, starting_wealth=sum([int(x) for x in captable.values()]))
    images.append(graphs.line_compare(rline_data, bline_data, 7))


    # Make bell curve
    images.append(graphs.bell_compare(mu=red['ret'], mu2=blue['ret'], sigma=red['risk'], sigma2=blue['risk']))
    images.append(graphs.bell(mu=red['ret'], sigma=red['risk']))


    # Inject variables into LaTeX report
    report.latex_pickle_dump(red, blue, new_pie)


    def neat(portfolios):
        def n(p):
            p = array(p)
            p = np.round(p,2)
            p = p.tolist()
            return p
        portfolios = [n(p) for p in portfolios]
        return portfolios


    portfolios = neat(ribs['port'])

    p = np.asmatrix(np.mean(daily_data, axis=1))
    C = np.asmatrix(np.cov(daily_data))
    matrices = (p, C)

    with open("matrices.pickle", 'wb') as matrix_pickle:
        pickle.dump(matrices, matrix_pickle)

    return images, portfolios, ribs['ret'], ribs['risk']