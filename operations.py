#  MATH OPERATIONS FOR USE IN GRAPHS AND MARKOWITZ
import numpy as np
import statistics as s


def mprint(name, x):
    print(name + ":\n", x, "\n", flush=True)


def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)


def AVG_annualize(daily_data,func):
    ATD=252
    means=[]

    for i in range(0,daily_data.shape[1],ATD):
        new_mean = func(daily_data[:,i:i+ATD]/daily_data[:,i])
        means.append(new_mean)

    means = np.mean(means,axis=0)

    return means


def AAR(daily_data):
    def ez_mean(d):
        return np.mean(d,axis=1)
    return AVG_annualize(daily_data,ez_mean)


def AC(daily_data):
    def ez_cov(d):
        return np.cov(d)
    return AVG_annualize(daily_data,ez_cov)


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


def portfolio_performance(daily_data, weights):
    # p = AAR(daily_data)
    p = np.asmatrix(np.mean(daily_data,axis=1))
    w = np.asmatrix(weights)
    C = np.asmatrix(np.cov(daily_data))
    # C = AC(daily_data)

    #calculates mean earnings (mu) and risk (sigma)
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    mu = np.asscalar(np.squeeze(np.asarray(mu)))
    sigma = np.asscalar(np.squeeze(np.asarray(sigma)))

    return mu, sigma


def montecarlo(mu, std, term, trials, starting_wealth=1):
    data = {period: [] for period in range(term+1)}

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