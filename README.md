# Portfolio Optimizer (by Greenstar Group)

![GreenstarBanner](/static/img/GreenstarBanner.png)



## What is Greenstar?

This is an open source software working off of yahoo finance data. 

It analyses your financial portfolio, and gives recommendations + reporting on how to rebalance your portfolio.

It does this looking at the bigger picture, the 18 asset classes.

It asks the following question :

> How much do you have invested in each of the 18 asset classes?

It then suggests a rebalancing of your assets based on your risk-return appetite.

It then generates a multi page report for you to understand the recommendation.



## How to use



### 1. Run the Docker Container

```shell
# install docker
# clone the repository, and cd into it. then run :
docker-compose up --build
```

![docker-compose](/documentation_gifs/docker-compose.gif)



### 2. Open the finance app in your web browser.

![OpenFinance](/documentation_gifs/OpenFinance.gif)

*The CRM has been moved to web10, you can check that out too!*

### 3. Enter your current portfolio breakdown by asset class.

![EnterForm](/documentation_gifs/EnterForm.gif)

### 4. Run Optimizer + Adjust Risk - Return

![ReportGen]![Run Markowitz](/documentation_gifs/Run Markowitz.gif)(C:\Users\jacks\OneDrive\Documents\GitHub\greenstar-financial\documentation_gifs\ReportGen.gif



### 5. Generate Financial Report For Yourself

![ReportGen](/documentation_gifs/ReportGen.gif)



Thank you for using! Please give this repo a star :)
