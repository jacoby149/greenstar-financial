# Portfolio Optimizer (by Greenstar Group)

![GreenstarBanner](/static/img/GreenstarBanner.png)



## What is Greenstar?

This is an open source software working off of yahoo finance data. 

It analyses your financial portfolio, and gives recommendations + reporting on how to rebalance your portfolio.

It does this looking at the bigger picture, the 18 asset classes.

It asks the following question :

> How much do you have invested in each of the 18 asset classes?

It then suggests a rebalancing of your assets based on your risk-return appetite.

It then generates a <a href="/pdfs/examples/John Doe Report.pdf">multi page report</a> for you to understand the recommendation.



## How to use



### 1. Run the Docker Container

```shell
# install docker
# clone the repository, and cd into it. then run :
docker-compose up --build
```

![docker-compose](/documentation_gifs/docker-compose.gif)



### 2. Open the financial planner app in your web browser.

Once the docker container is running, the financial application should be running on port 80. Go to localhost:80 in your web browser, and press the finance log in button. This will then redirect you to the Greenstar Group Financial Planner.

![OpenFinance](/documentation_gifs/OpenFinance.gif)

*The CRM has been moved to web10, you can check that out too!*



### 3. Enter your current portfolio breakdown by asset class.

#### Enter your info.

Enter your name, birthday, and how long you are willing to invest your money without being able to take the money out. The financial report will configure the Monte Carlo simulated graphs in the report to the investment term you put in.

#### Enter your Assets

Your portfolio will be made of some breakdown of the 18 asset classes, i.e. if you own Facebook Stock in 2023, that falls under Large Cap Value. Figure out what asset class each of your assets falls under, and put the total monetary amounts of each asset class that you own in the form.

![EnterForm](/documentation_gifs/EnterForm.gif)



### 4. Run Optimizer + Adjust Risk - Return

#### Running the computation.

After you fill out the form, hit the Run Computation button. If you are running it for the first time, it might take longer. Once the Frontier Chart shows up, you can click on the curve, and click the Run Computation button again to get recommendations tuned to your risk return appetite.

![Run Markowitz](/documentation_gifs/Run Markowitz.gif)

#### Efficient Frontier Chart

The software generates an interactive efficient frontier chart, generated via. convex optimization over the covariances / returns of all of the asset classes. The chart shows generic portfolios as gold dots, your current portfolio as a blue dot, and the optimized suggestion as a red dot. You can click on the interactive efficient frontier curve and re run the computation to adjust the suggestion, you will see the red dot move to where you clicked after the computation.

#### Asset Allocation Pie Charts 

You will see a current pie chart showing how your portfolio is currently allocated among the 18 asset classes and a prescribed pie chart showing how the software recommends you should rebalance your portfolio. 

#### Asset Class Data

You will see an overview of all of the daily data of the asset classes since 2013. The software uses this daily data to make the portfolio rebalancing decisions.

#### Monte Carlo Line Chart + Bell Curves

You will see a line graph that is the result of a Monte Carlo simulation showing your improvement in expected returns, and additionally a bell curve chart illustrating the improvement of your current portfolio. A narrower bell indicates that a portfolio is less risky, while the position of the bell indicates how much expected return their is.



### 5. Generate Financial Report For Yourself

You can generate a financial report PDF for yourself, that you can print out and use as a reference for yourself. The financial report is not financial advise, it is just an informational report for you to learn more about rebalancing your assets.

![ReportGen](/documentation_gifs/ReportGen.gif)



Hope you enjoyed, thanks!
