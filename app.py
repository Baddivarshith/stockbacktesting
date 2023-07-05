# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:32:35 2022

@author: varsh
"""
pip install yfinance 
import pandas as pd 
import numpy as np 
import yfinance as yf 
import streamlit as st 
import vectorbt as vbt 
import matplotlib.pyplot as plt
import plotly
from flask import Flask,render_template
import ta 
import plotly.express as px
import plotly.graph_objects as go

st.title('stock analysis')
ticker_name=st.text_input('Enter stock ticker:','INFY.NS')
ticker = yf.Ticker(ticker_name)
info = st.selectbox("info: ",
                     ['dividends', 'cashflow', 'balancesheet','financials'])
if info=='dividends':
    st.write(ticker.dividends)
elif info=='cashflow':
    st.write(ticker.cashflow)
elif info=='financials':
    st.write(ticker.financials)
else:
    st.write(ticker.balancesheet)    


stock_name=st.text_input('Enter stock ticker:','TCS.NS')
stock=yf.download(stock_name)
stock_return = vbt.Portfolio.from_holding(stock['Close'].loc['2003':], init_cash=100)
st.write('Total returns of stock :')
st.write(stock_return.total_profit())
fig=px.line(stock,x=stock.index,y='Close')
st.plotly_chart(fig, use_container_width=True)
def goldencrossover(close):
    fast_ma = vbt.MA.run(close, 50, short_name='fast_ma')
    slow_ma = vbt.MA.run(close, 200, short_name='slow_ma')
    buy = fast_ma.ma_crossed_above(slow_ma)
    sell = fast_ma.ma_crossed_below(slow_ma)
    pf=vbt.Portfolio.from_signals(stock['Close'].loc['2003':], buy.loc['2003':], sell.loc['2003':], init_cash=100)
    return pf


def rsi(close):
    RSI=ta.momentum.RSIIndicator(close, 14)
    rsi=RSI.rsi().dropna()
    sell =(rsi>70).astype(int).diff()
    buy=(rsi<50).astype(int).diff()
    pf=vbt.Portfolio.from_signals(stock['Close'].loc['2003':], buy.loc['2003':], sell.loc['2003':], init_cash=100)
    return pf


def bollingear(close):
   bollih=ta.volatility.bollinger_hband(close, 20,2,False)
   sell=ta.volatility.bollinger_hband_indicator(close, 20, 2, False)
   bolli_l=ta.volatility.bollinger_lband(close, 20, 2,False)
   buy=ta.volatility.bollinger_lband_indicator(close,20, 2, False)
   bolli_mvg=ta.volatility.bollinger_mavg(close,20, False)
   pf=vbt.Portfolio.from_signals(stock['Close'].loc['2003':], buy.loc['2003':], sell.loc['2003':], init_cash=100)
   return pf

indicator=st.selectbox("info: ",['BOLLI', 'Goldencrossover', 'RSI'])
if indicator=='BOLLI':
    img=bollingear(stock['Close']).plot(subplots='value')
    st.plotly_chart(img, use_container_width=True)
    st.write('total returns of strategy:')
    st.write(bollingear(stock['Close']).total_profit())
elif indicator=='Goldencrossover':
    img=goldencrossover(stock['Close']).plot(subplots='value')
    st.plotly_chart(img, use_container_width=True)
    st.write('total returns of strategy:')
    st.write(goldencrossover(stock['Close']).total_profit())
   
elif indicator=='RSI':
    img=rsi(stock['Close']).plot(subplots='value')
    st.plotly_chart(img, use_container_width=True)
    st.write('total returns of strategy:')
    st.write(rsi(stock['Close']).total_profit())
   
else:
    st.write('no indicator')


