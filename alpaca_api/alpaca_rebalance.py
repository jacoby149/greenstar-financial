"""
    Q : how about to reallocate an existing portfolio to the newly calculated weights?
    A : 
    
    To reallocate an existing portfolio to the newly calculated weights, you can follow these steps:

    1. Get current portfolio holdings:
    You can use the Alpaca API to fetch the current holdings of your portfolio using the "list_positions" method of the API client object.
"""
# get current portfolio holdings
positions = api.list_positions()

"""
2. Calculate target holdings:
   You can calculate the target holdings based on the optimal weights obtained from Markowitz portfolio optimization. For example, if the optimal weight for a stock is 10%, and you currently hold 100 shares of that stock, the target holding would be 110 shares (10% increase).
"""
# calculate target holdings
target_holdings = {}
for symbol, weight in cleaned_weights.items():
    target_shares = int(weight * 100000 / latest_prices[symbol])
    if symbol in [pos.symbol for pos in positions]:
        current_pos = [pos for pos in positions if pos.symbol == symbol][0]
        target_shares -= int(float(current_pos.qty))
    target_holdings[symbol] = target_shares

"""
   In the above code, we have calculated the target holdings for each stock in the portfolio based on the optimal weights obtained from Markowitz portfolio optimization. We have subtracted the current holdings from the target holdings to get the number of shares to buy or sell.

3. Place orders:
   Finally, you can use the Alpaca API to place orders to buy or sell stocks to reallocate the portfolio to the target holdings. You can use the "submit_order" method of the API client object to place the orders.
"""

# place orders to reallocate portfolio
for symbol, target_shares in target_holdings.items():
    if target_shares > 0:
        api.submit_order(
            symbol=symbol,
            qty=target_shares,
            side='buy',
            type='market',
            time_in_force='day'
        )
    elif target_shares < 0:
        api.submit_order(
            symbol=symbol,
            qty=abs(target_shares),
            side='sell',
            type='market',
            time_in_force='day'
        )

"""
In the above code, we have used the target holdings calculated in the previous step to place orders to buy or sell stocks to reallocate the portfolio.

That's it! With these steps, you can reallocate an existing portfolio to the newly calculated weights obtained from Markowitz portfolio optimization. Note that building a successful trading strategy requires significant research, testing, and deployment. It is also crucial to be mindful of the risks and limitations of algorithmic trading and to always work within safe monetary limits.
"""