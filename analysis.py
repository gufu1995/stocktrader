# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 21:53:56 2024

@author: Gunnar
"""
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_csv( filepath ):
    data = pd.read_csv( filepath )
    if 'Date' in data.columns:
        data = data.set_index( 'Date' )
    data = data.dropna(axis=1, how='all')
    return data


def correlation_investigation( dataframe, threshold = 0.85 ):
    
    correlation_matrix = dataframe.corr()
    
    # # Set up the matplotlib figure
    # plt.figure(figsize=(20, 15))

    # # Draw the heatmap
    # sns.heatmap(correlation_matrix, cmap='coolwarm')

    # plt.title('Correlation Matrix of S&P 500 Stocks')
    # plt.xlabel('Stocks')
    # plt.ylabel('Stocks')
    # plt.show()


    # Flatten the matrix and exclude self-correlations (diagonal elements)
    corr_values = correlation_matrix.values.flatten()
    corr_values = corr_values[corr_values != 1]
    
    # Plot the distribution
    plt.figure(figsize=(10, 6))
    plt.hist(corr_values, bins=100, color='skyblue', edgecolor='black')
    plt.title('Distribution of Correlation Coefficients')
    plt.xlabel('Correlation Coefficient')
    plt.ylabel('Frequency')
    plt.show()
    
    # Get pairs above the threshold
    high_corr_pairs = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
    high_corr_pairs = high_corr_pairs.stack()
    high_corr_pairs = high_corr_pairs[high_corr_pairs > threshold]
    
    # Display top 10 highly correlated pairs
    print("Top 10 highly correlated stock pairs:")
    print(high_corr_pairs.sort_values(ascending=False))
    
    
    return correlation_matrix
        

def __plot_tickers( data, ticker, period ):
    
    
    chart_filename = f"charts/{ticker}.png"

    # Plot and save the candlestick chart
    mpf.plot(data, type='candle', style='yahoo', # 'charles'
      title=f"{ticker} Stock Price - Last {period}",
      ylabel='Price (USD)',
      volume=True,
       mav=(20, 50),  # Moving averages
      figsize = (14,8),
      figscale=1.5,
      savefig=dict(fname=chart_filename, dpi=300),
      tight_layout=True)
    print(f"Saved candlestick chart for {ticker} to {chart_filename}")
