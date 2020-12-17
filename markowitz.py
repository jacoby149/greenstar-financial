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

from sympy.utilities.iterables import multiset_permutations

from datetime import date,timedelta,datetime

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

def yahoo_assets(tickers, info):
    # mprint("TICKERS",tickers)
    end_date = info['end_date']
    start_date = date(2007, 12, 19)

    tickers = " ".join(tickers)
    filename = "csv/yfinance" + str(end_date) + tickers + ".csv"

    print("collecting daily data:")
    if os.path.exists(filename):
        print(filename + " exists\n")
        yahoo = pd.read_csv(filename, index_col="Date")
    else:
        print("downloading data from yahoo\n")
        yahoo = yf.download(tickers, start=str(start_date), end=str(end_date))['Adj Close']
        yahoo.to_csv(filename, header=True)

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



#################################
#######  PORTFOLIO CALC  ########
#################################

def bundles(c,l,n,G,h):
    #all bundles of size l > c
    #-wa -wb -wc <= -.3
    #IS wa+wb+wc >= .3
    #all perms i.e.
    #[1,1,1,0,0,0],[1,0,1,1,0,0]...
    perms = list(multiset_permutations([1 if i<l else 0 for i in range(n)]))
    G_ext = -np.matrix(perms)
    #matrix of boundary c
    h_ext = -np.full((len(perms),1),c)

    #append the bundle boundaries.
    G = opt.matrix(np.vstack((G,G_ext)))
    h = opt.matrix(np.vstack((h,h_ext)))

    return G,h


def limits(G,h,book):
    n=book.shape[0]
    # [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    G_ext=np.eye(n)

    h_ext=book['upperlimit'].tolist()
    h_ext=np.matrix([h_ext])
    h_ext=h_ext.T

    # mprint("g_ext",G_ext)
    # mprint("g shape",G_ext.shape)
    # mprint("h_ext",h_ext)
    # mprint("h shape",h_ext.shape)

    # append limit constraints
    G = opt.matrix(np.vstack((G,G_ext)))
    h = opt.matrix(np.vstack((h,h_ext)))
    return G, h


def optimal_portfolio(daily_data,book):
    n = len(daily_data)
    daily_data = np.asmatrix(daily_data)
    mus = ops.get_mus(N=500, t=200, n=n)
    
    # Convert to cvxopt matrices
    S = opt.matrix(ops.AC(daily_data))

    #calculate annual average return (AAR)
    pbar = opt.matrix(ops.AAR(daily_data))


    # mprint("pbar",pbar)

    # all stocks are greater than zero.
    #w0 > 0, w1> 0 ... wn > 0
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))

    #add bundle boundaries bundles size l sum greater weight than c BUNDLE BUNDLE BUNDLE
    G,h = bundles(c=.25,l=n - n//4,n=n,G=G,h=h)

    #add limit constraints (i.e. no more than 10% in V.C. etc)
    G,h = limits(G,h,book)
    
    #all stocks add up to 1.
    #w1 + w2 + ... = 1
    A = opt.matrix(1.0, (1, n)) #all stocks add to 1.
    b = opt.matrix(1.0)
    

    # Calculate rib frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus]

    # Calculate risk and return for frontier using linear algebra solving
    returns = [blas.dot(pbar, p) - 1 for p in portfolios]
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


def get_weights(book):

    allocations = book['allocation'].tolist()
    allocations = [a / sum(allocations) for a in allocations]

    return allocations


def add_recommended(book, redbook, chosen, wealth):
    chosen_cash = [int(c*wealth) for c in chosen]

    chosen_dict = dict(zip(redbook['assetclass'],chosen_cash))
    book['recommended'] = book['assetclass'].map(chosen_dict)
    book['recommended'] = book['recommended'].apply(lambda x: int(0) if pd.isna(x) is True else int(x))

    # mprint('recommended book',book)

    return book


def add_change(book):
    current = book['allocation'].tolist()
    recommended = book['recommended'].tolist()
    change = [recommended[i] - current[i] for i, n in enumerate(current)]
    book['change'] = change

    # add column for display on final report
    book['infinal'] = [False if b == 0 else True for b in book['recommended']]

    return book


def frame_matrix(C, ybook):
    def hundredth(x):
        return round(x,2)

    C = pd.DataFrame(C).apply(hundredth)
    C.columns = ybook['latex'].tolist()
    C['ticker'] = ybook['latex'].tolist()
    C.set_index('ticker', inplace=True)
    del C.index.name

    return C


def frame_vector(v, ybook):
    def hundredth(x):
        return round(x,2)

    v = pd.DataFrame(v).apply(hundredth)
    v.columns = ybook['ticker']
    v.sort_values(by=0, axis=1, inplace=True)

    # mprint("p",v)

    return v


#################################
#######  MARKOWITZ RUN   ########
#################################

def dataframe_structures(book):
    # get structures for future strategy (red)
    redbook = book.loc[book['inred'] == True]
    rtickers = redbook['ticker'].tolist()

    # mprint('redbook',redbook)
    # mprint('rtickers',rtickers)

    # get structures for current strategy (blue)
    bluebook = book.loc[book['inblue'] == True]
    btickers = bluebook['ticker'].tolist()

    # mprint('bluebook',bluebook)
    # mprint('btickers',btickers)

    # get structures for yahoo's daily data (yahoo)
    ybook = book.loc[(book['inred'] == True) | (book['inblue'] == True)] #comment
    ytickers = ybook['ticker'].tolist()

    # mprint('ybook',ybook)
    # mprint('ytickers',ytickers)

    return redbook, rtickers, bluebook, btickers, ybook, ytickers


def markowitz_run(book, info):
    images = []
    redbook, rtickers, bluebook, btickers, ybook, ytickers = dataframe_structures(book)
    blue_weights = get_weights(bluebook)

    mprint('blue weights',blue_weights)
    mprint('blue assets',bluebook.assetclass)

    risk_level = int(info['risk'])
    wealth = sum([int(val) for val in bluebook.allocation.tolist()])
    info['wealth'] = wealth

    daily_data = yahoo_assets(book['ticker'].tolist(), info)
    red_data = yahoo_assets(rtickers, info)
    blue_data = yahoo_assets(btickers, info)
    yahoo_data = yahoo_assets(ytickers, info)

    def get_frontier_data():
        limits = [str(x) for x in book['upperlimit'].tolist()]
        filename = "models/" + str(info['end_date']) + " ".join(limits) + ".pickle"

        if os.path.exists(filename):
            print(filename + " exists\n")
            with open(filename, 'rb') as model_pickle:
                portfolios, returns, risks = pickle.load(model_pickle)
        else:
            # get ribs data (frontier)
            portfolios, returns, risks = optimal_portfolio(red_data,redbook)

        # get wheats data (frontier)
        means, stds = np.column_stack([get_rand_portfolio(red_data) for _ in range(500)])

        # get red data (frontier)
        ret_new, risk_new = returns[risk_level], risks[risk_level]

        # get blue data (frontier)
        ret_curr, risk_curr = ops.portfolio_performance(blue_data,weights=blue_weights)

        # pack dictionary for quick unload
        red = {"ret": ret_new, "risk": risk_new}
        blue = {"ret": ret_curr, "risk": risk_curr, "weights": blue_weights}
        wheat = {"ret": means, "risk": stds}
        ribs = {"ret": returns, "risk": risks, 'port': portfolios}

        with open(filename, 'wb') as model_pickle:
            model_variables = (portfolios, returns, risks)
            pickle.dump(model_variables, model_pickle)

        return red, blue, wheat, ribs
    mprint("FRONTIER START",datetime.now())
    red, blue, wheat, ribs = get_frontier_data()
    mprint("FRONTIER FINISH",datetime.now())


    # remapping to relevant assets
    old_assets = bluebook['assetclass'].tolist()
    assets = redbook['assetclass'].tolist()

    # get pie data
    chosen_rib = ribs['port'][risk_level]
    future_pie_data = dict(zip(redbook.assetclass,chosen_rib))
    new_pie = {asset: future_pie_data[asset] for asset in future_pie_data if future_pie_data[asset] > 0.0005}
    ol_pie = dict(zip(bluebook.assetclass, blue_weights))


    # make frontier graph
    images.append(graphs.frontier(red, blue, wheat, ribs))


    # make pie graphs
    images.append(graphs.pie(new_pie, 'piefuture'))
    images.append(graphs.pie(ol_pie, 'pie'))


    # Make noise graph
    images.append(graphs.noise(yahoo_data, assets))


    # Make line graphs
    mprint("MONTECARLO START",datetime.now())
    rline_data = ops.montecarlo(mu=red['ret'], std=red['risk'], term=1, trials=1000, starting_wealth=wealth)
    bline_data = ops.montecarlo(mu=blue['ret'], std=blue['risk'], term=1, trials=1000, starting_wealth=wealth)
    images.append(graphs.line_compare(rline_data, bline_data))


    rline_data = ops.montecarlo(mu=red['ret'], std=red['risk'], term=7, trials=1000, starting_wealth=wealth)
    bline_data = ops.montecarlo(mu=blue['ret'], std=blue['risk'], term=7, trials=1000, starting_wealth=wealth)
    images.append(graphs.line_compare(rline_data, bline_data, 7))
    mprint("MONTECARLO FINISH",datetime.now())

    # write montecarlo data to info
    info['rlinedata'] = rline_data
    info['blinedata'] = bline_data



    # Make bell curve
    images.append(graphs.bell_compare(mu=red['ret'], mu2=blue['ret'], sigma=red['risk'], sigma2=blue['risk']))
    images.append(graphs.bell(mu=red['ret'], sigma=red['risk'], title='future',color='g',legend='Recommended'))
    images.append(graphs.bell(mu=blue['ret'], sigma=blue['risk'], legend='Current'))


    # get matrices
    p = np.asmatrix(np.mean(yahoo_data, axis=1))
    p = frame_vector(p, ybook)
    info['p'] = p

    #correlation matrix rather than covariance matrix :)
    
    cov = np.asmatrix(ops.AC(red_data))
    C = np.asmatrix(np.corrcoef(red_data))
    C = frame_matrix(C, redbook)
    r = np.asmatrix(np.sqrt(np.diag(cov)))
    r = frame_vector(r, redbook)
    info['r'] = r


    # update book
    book = add_recommended(book, redbook, chosen_rib, wealth)
    book = add_change(book)


    # Send variables to report.py for LaTeX injection
    report.pickle_dump(red, blue, C, book, info)


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