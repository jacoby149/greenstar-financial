#  MATH OPERATIONS FOR USE IN GRAPHS AND MARKOWITZ
import numpy as np
import scipy as sp
import statistics as s


def mprint(name, x):
    print(name + ":\n", x, "\n", flush=True)


def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

"""
def AAR(daily_data):
    ATD=252
    means=[]
    # mprint("ddshape",daily_data.shape)
    # mprint("dd",daily_data)

    for i in range(0,daily_data.shape[1],ATD):
        new_mean = np.mean(daily_data[:,i:i+ATD]/daily_data[:,i].reshape(-1,1),axis=1)
        means.append(new_mean)

    #Geometric mean
    means = sp.stats.mstats.gmean(means)

    return means
    """

def AAR(daily_data):
    ATD = 252
    new = daily_data[:,-1]
    old = daily_data[:,0]
    years = daily_data.shape[1]/ATD
    net = (new/old)
    # mprint("net",net)
    yearly = np.power(net,[1/years])
    # mprint("INCREASE",yearly)
    return yearly



def AC(daily_data):
    ATD=252
    cov=[]
    for i in range(0,daily_data.shape[1],ATD):
        # new_cov = np.cov(daily_data[:,i:i+ATD]/daily_data[:,i].reshape(-1,1))   # This shit ain't work
        new_cov = np.cov(daily_data[:,i:i+ATD])
        cov.append(new_cov)

    cov = np.mean(cov,axis=0)

    return cov


def get_mus(N=500, t=200, n=None):
    if n is None:
        n = 18
    if 0 <= n <= 7:
        power = n + 2
    else:
        power = 9.0
    #the first 20 portfolios are
    mus = [10**(power * b/N - 1.0) for b in range(0,t)]
    return mus


def portfolio_performance(daily_data, weights ,p , C):
    w = np.asmatrix(weights)

    #calculates mean earnings (mu) and risk (sigma)
    mu = w * p.reshape(-1,1)
    sigma = np.sqrt(w * C * w.T)

    mu = np.asscalar(np.squeeze(np.asarray(mu))) - 1
    sigma = np.asscalar(np.squeeze(np.asarray(sigma)))

    return mu, sigma


def montecarlo(mu, std, term, trials, starting_wealth=1):
    data = {period: [] for period in range(term+1)}
    mu += 1
    for trial in range(trials):
        wealth = starting_wealth
        for period in range(term+1):
            data[period].append(wealth)
            wealth = wealth * np.random.normal(mu, std)

    for period in range(term+1):
        ret = sum(data[period]) / trials
        risk = s.stdev(data[period])
        data[period] = (ret, risk)

    return data