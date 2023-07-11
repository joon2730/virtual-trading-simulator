#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:21:14 2023

@author: yejoonjung
"""

import marketsimulator as ms
import datetime as dt
import pandas as pd

class VirtualTrade:
    def __init__(self, stocks, start_date=dt.datetime.today()-dt.timedelta(days=365), \
        end_date=dt.datetime.today(), frequency = "1h", transaction_fee_pct = 0.09):
        self.market = ms.Market(stocks, start_date, end_date, frequency)
        self.brokage = Brokage(self.market, transaction_fee_pct)

class Brokage:
    def __init__(self, market, transaction_fee_pct):
        self.market = market
        self.transaction_fee_pct = transaction_fee_pct
        self.accounts = {}
        
    def open_new_account(self, account_id, seed=1000):
        if account_id in self.accounts.keys():
            raise Exception("Error: id already exist (must be unique)")
        self.accounts[account_id] = Account(seed)    
        
    def buy(self, account_id, symbol, quantity):
        # identify account
        if not account_id in self.accounts.keys():
            raise Exception("Error: id not found")
        account = self.accounts[account_id]
        
        # compute payment amount
        price = self.market.adj_close(symbol)
        amount = quantity * price
        commission = self.transaction_fee_pct * amount
        total = amount + commission
        
        # perform transaction
        if account.cash_balance < total:
            raise Exception("Error: insufficient balance")
        account.cash_balance -= total
        
        # update portfolio
        if symbol in account.portfolio.keys():
            account.portfolio[symbol] += quantity
        else:
            account.portfolio[symbol] = quantity
            
        # record order history
        side = "BUY"
        account.add_order_history(self.market.current_datetime(), side, quantity, symbol, price, total, account.cash_balance)
        return (amount, commission, total)

    def sell(self, account_id, symbol, quantity):
        # identify account
        if not account_id in self.accounts.keys():
            raise Exception("Error: id not found")
        account = self.accounts[account_id]
        
        # compute amount incoming
        price = self.market.adj_close(symbol)
        amount = quantity * price
        commission = self.transaction_fee_pct * amount
        total = amount - commission
        
        # update portfolio
        if symbol not in account.portfolio.keys() or account.portfolio[symbol] < quantity:
            raise Exception("Error: insufficuent quantity held")
            account.portfolio[symbol] -= quantity
            
        # perform transaction
        account.cash_balance += total
        
        # record order history
        side = "SELL"
        account.add_order_history(self.market.current_datetime(), side, quantity, symbol, price, total, account.cash_balance)
        return (amount, commission, total)

    def account_summary(self, account_id):
        # identify account
        if not account_id in self.accounts.keys():
            raise Exception("Error: id not found")
        account = self.accounts[account_id]
        
        # compute value of tatal equity
        value_of_stock = 0
        for key in account.portfolio.keys():
            price = self.market.adj_close(key)
            value_of_stock += account.portfolio[key] * price
        total_equity = value_of_stock + account.cash_balance
        
        # compute return/gain/profit
        total_increase = total_equity/account.seed - 1
        total_profit = total_equity - account.seed
        return (round(total_equity, 2), round(account.cash_balance, 2), round(value_of_stock, 2), round(total_increase, 2), round(total_profit, 2), account.portfolio)
            
    
class Account:
    def __init__(self, seed):
        self.seed = seed
        self.cash_balance = seed
        self.portfolio = {}
        COLUMN_NAMES = ["side", "quantity", "symbol", "price", "total", "balance"]
        self.order_history = pd.DataFrame(columns=COLUMN_NAMES)
        
    def add_order_history(self, time_placed, side, quantity, symbol, price, total, balance):
        order_summary = [side, quantity, symbol, price, total, balance]
        pd.concat([self.order_history, pd.Series(order_summary, index=self.order_history.columns, name=time_placed)])
    
    