"""
    Q : how can i use alpace with markowitz portfolio optimization?
    A :
    To use Alpaca with Markowitz portfolio optimization, you can follow these steps:

    1. Install the required libraries:
    Firstly, you need to install the required Python libraries for Markowitz optimization. You can use NumPy and SciPy to perform the mathematical calculations required for optimization.

    ```bash
        pip install numpy scipy
    ```

    2. Authenticate API:
    Next, you need to authenticate Alpaca API using your API keys and create an instance of the Alpaca API client object.
"""
import alpaca_trade_api as tradeapi

# create a client object
api = tradeapi.REST('YOUR_API_KEY_ID', 'YOUR_SECRET_API_KEY', base_url='https://paper-api.alpaca.markets')

"""
    3. Get Historical Price data:
    You can use the Alpaca API to fetch historical price data for multiple stocks. Use the "get_barset" method of the API client object to get historical price data.
"""

# get historical price data
prices = api.get_barset(stock_symbols, 'day', limit=252).df

"""
   Here, we have specified the "limit" parameter to get the price data for the last 252 trading days.

4. Markowitz Portfolio Optimization:
   You can then use the price data to perform Markowitz portfolio optimization using the "Portfolio" class of the PyPortfolioOpt library. PyPortfolioOpt is a Python library for portfolio optimization.
"""

from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# calculate expected returns and sample covariance matrix
mu = expected_returns.mean_historical_return(prices)
S = risk_models.sample_cov(prices)

# optimize using a convex optimization algorithm
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

"""
   In the above code, we have used the "mean_historical_return" and "sample_cov" functions to calculate the expected returns and sample covariance matrix respectively. We then used the "EfficientFrontier" class to optimize the portfolio and get the optimal weights using the "max_sharpe" method. Finally, we used the "clean_weights" method to clean the weights and allocate the assets.

5. Place orders:
   You can use the Alpaca API to place orders using the optimal portfolio weights calculated in the previous step. You can use the "submit_order" method of the Alpaca API client object to place the orders.
"""

# get latest prices
latest_prices = get_latest_prices(prices)
weights = {symbol: weight for symbol, weight in cleaned_weights.items() if weight > 0}

# discretely allocate the assets
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=100000)
allocation, leftover = da.lp_portfolio()

# place orders
for symbol, shares in allocation.items():
    api.submit_order(
        symbol=symbol,
        qty=shares,
        side='buy',
        type='market',
        time_in_force='day'
    )

"""
   In the above code, we have used the "DiscreteAllocation" class of the PyPortfolioOpt library to allocate the assets discretely based on the optimal portfolio weights. We have then used the "submit_order" method of the Alpaca API client object to place the orders.

That's it! With these steps, you can use Alpaca with Markowitz portfolio optimization to trade stocks programmatically. Note that building a successful trading strategy requires significant research, testing, and deployment. It is also crucial to be mindful of the risks and limitations of algorithmic trading and to always work within safe monetary limits.

"""