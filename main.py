# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 21:59:19 2024

@author: Gunnar
"""

import analysis
import pandas as pd
import os


def main( ):   
    
    fetch_data = False
    
    os.makedirs('charts', exist_ok=True)
    
    if fetch_data:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        period= '10y'    
        interval = '1d'  
        data = analysis.analyze_tickers(tickers = tickers, save_csv = True, period = period, interval = interval, analysis_type = "d2d", plot_ticker = False )
    else:
        data = analysis.load_csv( "data/return_d.csv" )
    
    correlation_matrix = analysis.correlation_investigation( dataframe = data )
    
    return correlation_matrix, data

if __name__ == "__main__":
    correlation_matrix, data = main( )  