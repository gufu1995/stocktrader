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
import data_retreival as dr

def PLOT_complete_data( ticker, data, safe, filepath ):

    start_date = pd.to_datetime("2011-01-01 00:00:00")
    end_date = pd.to_datetime("2024-08-01 00:00:00")
    
    data = dr.DATA_FILTER_complete_csv_data_time( data_series = data, 
                                                 start_date = start_date, end_date = end_date )
    df = data.copy()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    df['STD20'] = df['Close'].rolling(window=20).std()
    df['UpperBB'] = df['MA20'] + (df['STD20'] * 2)
    df['LowerBB'] = df['MA20'] - (df['STD20'] * 2)
    

    # Plot Candlestick chart with Moving Averages and Bollinger Bands
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), dpi = 200,
                                   gridspec_kw={'height_ratios': [3, 1]})

    apd = [
        mpf.make_addplot(df['UpperBB'], ax=ax1),
        mpf.make_addplot(df['LowerBB'], ax=ax1),
           ]
    # Candlestick plot with Moving Averages and Bollinger Bands
    mpf.plot(df, type='candle', style='yahoo', 
             ax=ax1, volume=False, mav=(9, 20), addplot=apd)

    ax1.set_title(f'{ticker} Stock Price with Moving Averages and Bollinger Bands')

    # Plot daily returns
    ax2.plot(df.index, df['returns'], label='Daily Returns', color='blue')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax2.set_title('Daily Returns')
    ax2.legend(loc='best')

    plt.tight_layout()
    
    if safe:
        fig.savefig( filepath )
        plt.close( fig )
    else:
        plt.show()
    return


def ANALYSE_file( filepath ):

    data = dr.LOCAL_load_csv_data( filepath = filepath )
    
    ticker, date_format = dr.META_ANALYZE_local_filename( filename = filepath )

    filepath = f"charts/single/{ticker}_{date_format}.png"

    PLOT_complete_data( ticker = ticker, data = data, safe = True , filepath = filepath )



def EXECUTE_fn_filelist( filelist, function ):
    
    for file in filelist:
        function( file )

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
        
    
    
