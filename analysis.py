# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 21:53:56 2024

@author: Gunnar
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
import mplfinance as mpf


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url)
sp500_table = tables[0]
tickers = sp500_table['Symbol'].tolist()


os.makedirs('charts', exist_ok=True)

period = '1y'    # Last 5 years
interval = '1d'  # Daily data

for ticker in tickers[ : 2 ]:
    print(f"Fetching data for {ticker}...")
    try:
        # Download historical data
        data = yf.download(ticker, period=period, interval=interval)

        data = yf.download(ticker, period=period)

        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue

        data.index.name = 'Date'

        data['Typical_Price'] = (data['High'] + data['Low'] + data['Close']) / 3

        # Calculate the Cumulative Total Price Volume (Cumulative TPV)
        data['Cumulative_TPV'] = (data['Typical_Price'] * data['Volume']).cumsum()

        # Calculate the Cumulative Volume
        data['Cumulative_Volume'] = data['Volume'].cumsum()

        # Calculate VWAP
        data['VWAP'] = data['Cumulative_TPV'] / data['Cumulative_Volume']

        apdict = mpf.make_addplot(data['VWAP'], color='purple')

        # Prepare the file name
        chart_filename = f"charts/{ticker}.png"

        # Plot and save the candlestick chart
        mpf.plot(data, type='candle', style='yahoo', # 'charles'
         title=f"{ticker} Stock Price - Last {period}",
         ylabel='Price (USD)',
         volume=True,
         # mav=(20, 50),  # Moving averages
         figsize = (14,8),
         addplot=apdict,
         figscale=1.5,
         savefig=dict(fname=chart_filename, dpi=300),
         tight_layout=True)
        print(f"Saved candlestick chart for {ticker} to {chart_filename}")

    except Exception as e:
        print(f"An error occurred for {ticker}: {e}")