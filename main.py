#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 01:31:48 2023

@author: yejoonjung
"""

import virtualtrading as vt
import datetime as dt

##########################################
# Configration
# 
# Edit here to get any stocks you want
APPLE = "AAPL"
MICROSOFT = "MSFT"
TESLA = "TSLA"
NVIDIA = "NVDA"
META = "META"
ALPHABET = "GOOG"
stocks = [APPLE, MICROSOFT, TESLA]
#
# Edit here to set time period and interval
start = dt.datetime.today() - dt.timedelta(365 * 3)
end = dt.datetime.today()
freq = "1d"
##########################################

if __name__ == "__main__":
    LINE = ('-' * 32) + '\n'

    td = vt.VirtualTrade(stocks, start, end, freq, 0.09)
    id = "user1"
    td.brokage.open_new_account(id)

    while td.market.current_datetime() != end:
        print(LINE + str(td.market), end='')
        while True:
            try:
                command = input()
                if command == '':
                    break
                lst = command.strip().split()
                if lst[0] == 'buy':
                    receipt = td.brokage.buy(id, lst[1], int(lst[2]))
                    name = ['amount', 'commission', 'total paid']
                    print('Transaction Summary ---|')
                    for n, r in zip(name, receipt):
                        print(f'{n}: {r}')
                elif lst[0] == 'sell':
                    receipt = td.brokage.sell(id, lst[1], int(lst[2]))
                    name = ['amount', 'commission', 'total received']
                    print('Transaction Summary ---|')
                    for n, s in zip(name, receipt):
                        print(f'{n}: {r}')
                elif lst[0] == 'summary':
                    summ = td.brokage.account_summary(id)
                    name = ['total equity', 'cash balance', 'value of stock', 'total increase', 'total profit', 'portfolio']
                    print('Account Summary --------|')
                    for n, s in zip(name, summ):
                        print(f'{n}: {s}')
                elif lst[0] == 'candle':
                    for ticker in lst[1:]:
                        td.market.showCandleChart(ticker)
                elif lst[0] == 'line':
                    if len(lst[1:]) == 0:
                        td.market.showComparisonChart()
                    else:
                        td.market.showComparisonChart(lst[1:])
                else:
                    print("command not found")

            except ValueError as e:
                print(e)

        td.market.tick()
