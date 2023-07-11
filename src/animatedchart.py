#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 11:35:18 2023

@author: yejoonjung
"""

# importing libraries
import numpy as np
import time
import datetime as dt
import matplotlib.pyplot as plt
import marketsimulator as ms
import seaborn as sns

##################################################################
# modify here to set stocks, period, interval of interest
#
APPLE = "AAPL"
MICROSOFT = "MSFT"
TESLA = "TSLA"
NVIDIA = "NVDA"
META = "META"
ALPHABET = "GOOG"

stocks = [APPLE, MICROSOFT] # ... etc if you want

start = dt.datetime.today() - dt.timedelta(365 * 3)
end = dt.datetime.today()
freq = "1d"
#################################################################


market = ms.Market(stocks, start, end, freq)
data = market.get_ohlcv_dataframe(stocks[-1])

# to run GUI event loop
plt.ion()

# Set the Seaborn style
sns.set(style="darkgrid")

# here we are creating sub plots
fig, ax = plt.subplots(figsize=(8, 5))

# Loop
for _ in range(len(market.times)):
    ax.clear()
	
	# setting title
    plt.title("Change in Price of Major Stocks in Nasdaq", fontsize=20)

    # setting x-axis label and y-axis label
    plt.xlabel("Datetime")
    plt.ylabel("Price (usd)")

    # rotating the x-axis tick labels at 30 degree towards right
    plt.xticks(rotation=30, ha='right')

    for stock in stocks:
        # plot graph
        data = market.get_ohlcv_series(stock, "Adj Close")
        ax.plot(data.index, data, label=stock)
    ax.legend(loc='upper left', fancybox=True, framealpha=0.5)
	
    # adjust subplot to fit frame
    plt.tight_layout()
	
    # drawing updated values
    fig.canvas.draw()

    # This will run the GUI event
    # loop until all UI events
    # currently waiting have been processed
    fig.canvas.flush_events()

    market.tick()

input("press enter to close ...")
    

	

