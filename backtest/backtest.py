#backtest.py

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

from collections import OrderedDict
import pytz


def make_csvs(yahoo,tickers):
    for t in tickers:
        dest = "csvs/daily/" + t + ".csv"
        yahoo[t].to_csv(dest)
        print("added csv for "+t,flush=True)

    
def register_ingest():
    import os
    print("Ingesting Bundle",flush=True)
    cmd = "zipline -e extension.py ingest -b provins_bundle && zipline bundles"
    os.system(cmd)
    print("Bundle Ingested",flush=True)
    

def backtest(risk_level=50):
    environ = os.environ

    tickers = ['IBM', 'SBUX', 'XOM', 'AAPL', 'MSFT',]
    
    start_date='2005-01-02'
    end_date='2015-01-02'
    
    yahoo = yf.download(" ".join(tickers),group_by = 'ticker',start=start_date, end=end_date)
    yahoo.columns.set_levels(['adj close','close','high','low','open','volume',],level=1,inplace=True)
    
    #make_csvs(yahoo,tickers)
    register_ingest()
    
    #bundle_data = bundles.load("custom-csvdir-bundle")
    #print(data['MSFT'])
    #print(data['AAPL'])
    #yahoo.plot()
    #plt.ylabel('price in $')
    #plt.legend(tickers);


    # Next, we'll create a `zipline` algorithm by defining two functions: `initialize()`, which is called once before the simulation starts, and `handle_data()`, which is called for every trading bar. We then instantiate the algorithm object.
    # 
    # If you are confused about the syntax of `zipline`, check out the [tutorial](http://www.zipline.io/beginner-tutorial.html).

    # In[ ]:

    def initialize(context):
        '''
        Called once at the very beginning of a backtest (and live trading). 
        Use this method to set up any bookkeeping variables.
        
        The context object is passed to all the other methods in your algorithm.

        Parameters

        context: An initialized and empty Python dictionary that has been 
                augmented so that properties can be accessed using dot 
                notation as well as the traditional bracket notation.
        
        Returns None
        '''
        # Turn off the slippage model
        set_slippage(slippage.FixedSlippage(spread=0.0))
        # Set the commission model (Interactive Brokers Commission)
        set_commission(commission.PerShare(cost=0.01, min_trade_cost=1.0))
        context.tick = 0
        context.assets = symbols(*tickers)
        
    return_weights = []
    def handle_data(context, data):
        '''
        Called when a market event occurs for any of the algorithm's 
        securities. 

        Parameters

        data: A dictionary keyed by security id containing the current 
            state of the securities in the algo's universe.

        context: The same context object from the initialize function.
                Stores the up to date portfolio as well as any state 
                variables defined.

        Returns None
        '''
        
        # Allow history to accumulate 100 days of prices before trading
        # and rebalance every day thereafter.
        context.tick += 1
        look_back = 365
        rebalance_increment = 365
        if context.tick % rebalance_increment :
            return
        # Get rolling window of past prices and compute returns
        prices = data.history(context.assets, 'price', look_back, '1d').dropna()
        returns = prices.pct_change().dropna()
        try:
            # Perform Markowitz-style portfolio optimization
            portfolios, _, _ = optimal_portfolio(returns.T)
            #least risk portfolio
            portfolios.reverse()
            weights = portfolios[risk_level]

            r_w = neat(copy.deepcopy(portfolios))[risk_level]

            #weights = [w[0] for w in weights] #get the weights as an array
            #print("Calculated Weights : ",weights)
            # Rebalance portfolio accordingly
            return_weights.append(r_w)
            for stock, weight in zip(prices.columns, weights):
                order_target_percent(stock, weight)
        except ValueError as e:
            # Sometimes this error is thrown
            # ValueError: Rank(A) < p or Rank([P; A; G]) < n
            pass
            
    # Instantinate algorithm        
    #algo = zipline.run({},initialize=initialize, handle_data=handle_data)
    # Run algorithm
    #results = algo.run(data.swapaxes(2, 0, 1))
    start = pd.Timestamp(2005, 1, 1)
    start = start.tz_localize(tz='UTC')
    end = pd.Timestamp(2015, 1, 1)
    end = end.tz_localize(tz='UTC')
    capital_base = 1000000
    results = zipline.run_algorithm(start,end,initialize,capital_base,handle_data,bundle="provins_bundle")
    print("Ran Algorithm!")
    #print(results)
    #print("Plotted portfolio!")
    stock_plot = plt_to_img(plt)
    weights = results.portfolio_value.plot()
    weight_plot = plt_to_img(plt)
    weights = "<h1>Weights</h1>"
    for w in return_weights:
        weights = weights + "<br>"
        for i in range(len(tickers)):
            weights = weights + " || {} : {}".format(tickers[i],w[i])
    return weights,[stock_plot, weight_plot]  #arr[arr > 255] = x

    # As you can see, the performance here is quite good, even through the 2008 financial crisis. This is most likey due to our universe selection and shouldn't always be expected. Increasing the number of stocks in the universe might reduce the volatility as well. Please let us know in the comments section if you had any success with this strategy and how many stocks you used.

    # ## Conclusions
    # 
    # In this blog, co-written by Quantopian friend [Dr. Thomas Starke](http://drtomstarke.com/), we wanted to provide an intuitive and gentle introduction to Markowitz portfolio optimization which still remains relevant today. By simulating various random portfolios we have seen that certain portfolios perform better than others. Convex optimization using `cvxopt` allowed us to then numerically determine the portfolios that live on the *efficient frontier*. The zipline backtest serves as an example but also shows compelling performance.
    # 
    # ## Next steps
    # 
    # * Clone this notebook in the [Quantopian Research Platform](http://blog.quantopian.com/quantopian-research-your-backtesting-data-meets-ipython-notebook/) and run it on your own to see if you can enhance the performance. 
    # * You can also download just the notebook for use in your own environment [here]().
    # * In a future blog post we will outline the connections to Kelly optimization which also tells us the amount of leverage to use.
    # * We have added an optimization API which you can find [here](https://www.quantopian.com/posts/optimize-api-now-available-in-algorithms).

    # *This presentation is for informational purposes only and does not constitute an offer to sell, a solicitation to buy, or a recommendation for any security; nor does it constitute an offer to provide investment advisory or other services by Quantopian, Inc. ("Quantopian"). Nothing contained herein constitutes investment advice or offers any opinion with respect to the suitability of any security, and any views expressed herein should not be taken as advice to buy, sell, or hold any security or as an endorsement of any security or company.  In preparing the information contained herein, Quantopian, Inc. has not taken into account the investment needs, objectives, and financial circumstances of any particular investor. Any views expressed and data illustrated herein were prepared based upon information, believed to be reliable, available to Quantopian, Inc. at the time of publication. Quantopian makes no guarantees as to their accuracy or completeness. All information is subject to change and may quickly become unreliable for various reasons, including changes in market conditions or economic circumstances.*
