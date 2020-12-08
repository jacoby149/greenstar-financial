#  MATH OPERATIONS FOR USE IN GRAPHS AND MARKOWITZ
import numpy as np

def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)


def get_mus(N, t, n):
    N = 400            # Bigger N, bigger upper range, less lower range and less control. Smaller N, smaller range more control, more lower values
    if 0 <= n <= 7:
        power = n + 9
    else:
        power = 9.0
        #the first 20 porfolios are
    mus = [10**(power * t/N - 1.0) for t in range(0,200)]
    return mus


def portfolio_performance(daily_data, weights):
    p = np.asmatrix(np.mean(daily_data, axis=1))
    w = np.asmatrix(weights)
    C = np.asmatrix(np.cov(daily_data))

    #calculates mean earnings (mu) and risk (sigma)
    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    mu = np.asscalar(np.squeeze(np.asarray(mu)))
    sigma = np.asscalar(np.squeeze(np.asarray(sigma)))

    return mu, sigma


def montecarlo(mu, std, term, trials, starting_wealth=1):
    sums = {period: 0 for period in range(term+1)}

    for trial in range(trials):
        wealth = starting_wealth
        for period in range(term+1):
            sums[period] += wealth
            wealth = wealth * np.random.normal(mu, std)

    for period in range(term+1):
        sums[period] = sums[period] / trials

    return sums