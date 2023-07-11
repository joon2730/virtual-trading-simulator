#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:16:05 2023

@author: yejoonjung
"""

import datetime as dt
import yfinance as yf
import pandas as pd
import chart

class Market:
    
    def __init__(self, tickers, start_date, end_date, frequency):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.index = 0
        self.charts = []
        
        # download data
        self.ohlcv_data = {}
        for ticker in tickers:
            self.ohlcv_data[ticker] = yf.download(ticker, start_date, end_date)
        self.times = self.ohlcv_data[tickers[-1]].index


    
    def current_datetime(self):
        return self.times[self.index]
    
    def previous_datetime(self, delta=1):
        if self.index - delta < 0:
            raise ValueError()
        return self.times[self.index - delta]
        
    def open(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'Open', datetime)
    
    def high(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'High', datetime)

    def low(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'Low',datetime)

    def close(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'Close', datetime)
    
    def adj_close(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'Adj Close', datetime)

    def volume(self, symbol, datetime=None):
        if not datetime:
            datetime = self.current_datetime()
        return self.get_ohlcv(symbol, 'Volume', datetime)
    
    def get_ohlcv(self, symbol, ohlcv, datetime):
        return self.ohlcv_data[symbol][ohlcv][datetime]

    def get_ohlcv_series(self, symbol, ohlcv):
        data = self.ohlcv_data[symbol][ohlcv]
        return data.dropna(axis=0,how='any').loc[:self.current_datetime()]
    
    def get_ohlcv_dataframe(self, symbol):
        return self.ohlcv_data[symbol].dropna(axis=0,how='any').loc[:self.current_datetime()]

    def tick(self):
        self.index += 1
        for i, chrt in enumerate(self.charts):
            if not chrt.is_open:
                self.charts.pop(i)
                continue
            chrt.update()

    def __str__(self):
        repr = f'Market on {self.current_datetime().strftime("%m/%d/%Y, %H:%M:%S")}\n'
        for ticker in self.tickers:
            ret = None
            if self.index == 0 or self.adj_close(ticker) == self.adj_close(ticker, self.previous_datetime()):
                ret = '--'
            else:
                ret = round((self.adj_close(ticker) / self.adj_close(ticker, self.previous_datetime())) - 1, 2)
            repr += f'{ticker}: ({ret}%) ${round(self.adj_close(ticker), 2)}\n'
        return repr

    # ohlcv: one of 'Open' 'High' 'Low' 'Close' 'Adj Close' and 'Volume'
    def showComparisonChart(self, tickers=None, kind="Adj Close"):
        if tickers == None:
            tickers = self.tickers
        chrt = chart.ComparisonChart(self, tickers, kind)
        self.charts.append(chrt)
        chrt.update()
        return chrt

    def showCandleChart(self, ticker):
        if not ticker in self.tickers:
            raise ValueError()
        chrt = chart.CandleChart(self, ticker)
        self.charts.append(chrt)
        chrt.update()
        return chrt

