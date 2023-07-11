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

APPLE = "AAPL"
MICROSOFT = "MSFT"
TESLA = "TSLA"
NVIDIA = "NVDA"
META = "META"
ALPHABET = "GOOG"

stocks = [APPLE, MICROSOFT]
start = dt.datetime.today() - dt.timedelta(365 * 3)
end = dt.datetime.today()
freq = "1d"

#################################################################

market = ms.Market(stocks, start, end, freq)

data = market.get_ohlcv_dataframe(APPLE)

print(data['Adj Close'])

# # to run GUI event loop
# plt.ion()

# # Set the Seaborn style
# sns.set(style="darkgrid")

# # here we are creating sub plots
# fig, ax = plt.subplots(figsize=(8, 4))

# # Loop
# for _ in range(len(market.times)):
#     ax.clear()
	
# 	# setting title
#     plt.title("Change in Adj Close Price of Major Stocks in Nasdaq", fontsize=20)

#     # setting x-axis label and y-axis label
#     plt.xlabel("Date")
#     plt.ylabel("Price (usd)")

#     for stock in stocks:
#         # plot graph
#         data = market.adj_close(stock)
#         ax.plot(data.index, data, label=stock)
#     ax.legend(loc='upper left', fancybox=True, framealpha=0.5)
	
#     # adjust subplot to fit frame
#     plt.tight_layout()
	
#     # drawing updated values
#     fig.canvas.draw()

#     # This will run the GUI event
#     # loop until all UI events
#     # currently waiting have been processed
#     fig.canvas.flush_events()

#     market.tick()

# input()
    

	

