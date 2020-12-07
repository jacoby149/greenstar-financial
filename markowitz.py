# adapted quantopian markowitz code


# in-house
import graphs
import operations as ops
import report


from urllib.request import urlopen

#markowitz requirements.
import numpy as np
from numpy import array
from numpy import isnan

from datetime import date,timedelta


import pickle

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
    print("TICKERS :", tickers, flush=True)
    end_date = date.today()
    d = timedelta(days=1800)
    start_date = end_date - d

    labels = " ".join(tickers)
    yahoo = yf.download(labels, start=str(start_date), end=str(end_date))['Adj Close']
    yahoo.to_csv('tickers.csv')

    # print("yahoo data: ", yahoo.values, flush=True)
    # print("yahoo shape: ", yahoo.shape, flush=True)
    # print("yahoo type: ", type(yahoo), flush=True)
    # print(flush=True)

    def clean(yahoo):
        yahoo = yahoo.to_numpy()
        yahoo = np.reshape(yahoo, (yahoo.shape[0], -1))
        yahoo = yahoo / yahoo[0]

        # Sets nan values to value on first day listed (after normalization)
        findnans = isnan(yahoo)
        yahoo[findnans] = 1

        yahoo = yahoo.T
        # print("T shape: ", yahoo.shape, flush=True)
        return yahoo

    yahoo = clean(yahoo)
    return yahoo, labels


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

    return portfolios,returns,risks


def get_rand_portfolio(daily_data):
    # Returns the mean and standard deviation of returns for a random portfolio
    return ops.portfolio_performance(daily_data, ops.rand_weights(daily_data.shape[0]))


def customer_port_weights(captable):
    if captable is None:
        return [.2, .3, .2, .3]
    allocations = [int(captable[x]) for x in captable if "X".casefold() not in captable[x].casefold() and captable[x] != '']
    allocations = [a / sum(allocations) for a in allocations]
    # print("allocations: ", allocations)
    return allocations


def old_weights(captable):
    if captable is None:
        return [.2, .3, .2, .3]

    allocations = [captable[x] for x in captable if captable[x] != '']
    for i, item in enumerate(allocations):
        if 'X' in item:
            item = item[:-1]
        allocations[i] = int(item)

    allocations = [a / sum(allocations) for a in allocations]
    return allocations



#################################
#######  MARKOWITZ RUN   ########
#################################


def markowitz_run(daily_data=random_assets(), tickers=None, captable=None, risk_level=50, old_tickers=None):
    if tickers is not None:
        daily_data, labels = yahoo_assets(tickers)
        labels = labels.split(" ")
    else:
        labels = ["F", "A", "N", "g"]

    images = []

    def get_frontier_data():
        # get wheats data (frontier)
        means, stds = np.column_stack([get_rand_portfolio(daily_data) for _ in range(500) ])

        # get ribs data (frontier)
        portfolios, returns, risks = optimal_portfolio(daily_data)

        # get red data (frontier)
        ret_new, risk_new = [returns[risk_level]*100], [risks[risk_level]*100]

        # get blue data (frontier)
        weights = customer_port_weights(captable)
        ret_curr, risk_curr = ops.portfolio_performance(daily_data,weights=weights)

        # pack dictionary for quick unload
        red = {"ret": ret_new, "risk": risk_new}
        blue = {"ret": ret_curr, "risk": risk_curr, "weights": weights}
        wheat = {"ret": means, "risk": stds}
        ribs = {"ret": returns, "risk": risks, 'port': portfolios}

        return red, blue, wheat, ribs


    red, blue, wheat, ribs = get_frontier_data()


    # make frontier graph
    images.append(graphs.frontier(red, blue, wheat, ribs))


    # make pie graphs
    fpd = dict(zip(labels, ribs['port'][risk_level]))
    new_pie = {label: fpd[label] for label in fpd if fpd[label] > 0.0005}
    ol_pie = dict(zip(old_tickers, old_weights(captable)))

    images.append(graphs.pie(new_pie, 'piefuture'))
    images.append(graphs.pie(ol_pie, 'pie'))


    # Make noise graph
    images.append(graphs.noise(daily_data, labels))


    # Make line graphs
    ops.montecarlo(mu=1.05, std=.10, term=7, trials=1000000)
    ops.montecarlo(mu=1.05, std=0, term=7, trials=1000000)

    images.append(graphs.line())
    images.append(graphs.line(7))


    # Make bell curve
    images.append(graphs.normal())


    # Inject variables into LaTeX report
    report.latex_pickle_dump(red, blue)


    def neat(portfolios):
        def n(p):
            p = array(p)
            p = np.round(p,2)
            p = p.tolist()
            return p
        portfolios = [n(p) for p in portfolios]
        return portfolios


    portfolios = neat(ribs['port'])

    return images, portfolios, ribs['ret'], ribs['risk']