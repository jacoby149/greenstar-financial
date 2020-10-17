# coding: utf-8
#idea
#Make a bank on the dark web with 3% interest per year in USD.

#1. Zipline Related Trading & Backtesting
import zipline #– Zipline is a Pythonic algorithmic trading library. It is an event-driven system that supports both backtesting and live trading.

#Risk Analysis
import empyrical #– Common financial risk and performance metrics. Used by zipline and pyfolio.

#pyfolio is a Python library for performance and risk analysis of financial portfolios
import pyfolio

#library with alpha indicators compatible with zipline
import alphalens


#2. Ta Libs Related
import talib #– TA-Lib is widely used by trading software developers requiring to perform technical analysis of financial market data. It has an open-source API for python.

import pyalgotrade #– PyAlgoTrade is an event driven algorithmic trading Python library. Although the initial focus was on backtesting, paper trading is now possible incorporating TALIB

#Financial Instruments
import vollib
#– vollib is a python library for calculating option prices, implied volatility and greeks using Black, Black-Scholes, and Black-Scholes-Merton. vollib implements both analytical and numerical greeks for each of the three pricing formulae.


#Numerical, Statistical & Data Structures
import statsmodels #– Python module that allows users to explore data, estimate statistical models, and perform statistical tests.

import numpy #– NumPy is the fundamental package for scientific computing with Python. It is a first-rate library for numerical programming and is widely used in academia, finance, and industry. NumPy specializes in basic array operations.
import scipy #– SciPy supplements the popular Numeric module, Numpy. It is a Python-based ecosystem of open-source software for mathematics, science, and engineering. It is also used intensively for scientific and financial computation based on Python
import pandas #– The pandas library provides high-performance, easy-to-use data structures and data analysis tools for the Python programming language. Pandas focus is on the fundamental data types and their methods, leaving other packages to add more sophisticated statistical functionality

#I want to use zipline, talib, QSTK, and pyalgotrade for trading + backtests
# I want to use empyrical for risk analysis
# I want to use vollib for stochastic calc. options calculations