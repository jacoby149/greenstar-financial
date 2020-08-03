# coding: utf-8
#idea
#Make a bank on the dark web with 3% interest per year in USD.

#Numerical, Statistical & Data Structures
import numpy #– NumPy is the fundamental package for scientific computing with Python. It is a first-rate library for numerical programming and is widely used in academia, finance, and industry. NumPy specializes in basic array operations.
import scipy #– SciPy supplements the popular Numeric module, Numpy. It is a Python-based ecosystem of open-source software for mathematics, science, and engineering. It is also used intensively for scientific and financial computation based on Python
import pandas #– The pandas library provides high-performance, easy-to-use data structures and data analysis tools for the Python programming language. Pandas focus is on the fundamental data types and their methods, leaving other packages to add more sophisticated statistical functionality

#Financial Instruments
import vollib
#– vollib is a python library for calculating option prices, implied volatility and greeks using Black, Black-Scholes, and Black-Scholes-Merton. vollib implements both analytical and numerical greeks for each of the three pricing formulae.
import pynance #– PyNance is open-source software for retrieving, analyzing and visualizing data from stock and derivatives markets. It includes tools for generating features and labels for machine learning algorithms.

#Trading & Backtesting
import talib #– TA-Lib is widely used by trading software developers requiring to perform technical analysis of financial market data. It has an open-source API for python.
import zipline #– Zipline is a Pythonic algorithmic trading library. It is an event-driven system that supports both backtesting and live trading.
import QSTK #– Python-based open source software framework designed to support portfolio construction and management. It is built the QSToolKit primarily for finance students, computing students, and quantitative analysts with programming experience.
import pyalgotrade #– PyAlgoTrade is an event driven algorithmic trading Python library. Although the initial focus was on backtesting, paper trading is now possible
import pandas_talib #– A Python Pandas implementation of technical analysis indicators
import algobroker #– This is an execution engine for algo trading. The idea is that this python server gets requests from clients and then forwards them to the broker API.

#Risk Analysis
import pyfolio #– pyfolio is a Python library for performance and risk analysis of financial portfolios. It works well with the Zipline open source backtesting library.
import empyrical #– Common financial risk and performance metrics. Used by zipline and pyfolio.

# Time Series
import ARCH #– ARCH and other tools for financial econometrics in Python
import statsmodels #– Python module that allows users to explore data, estimate statistical models, and perform statistical tests.
import dynts #– A statistic package for python with emphasis on time series analysis. Built around numpy, it provides several back-end time series classes including R-based objects via rpy2.