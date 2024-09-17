# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:46:44 2024

@author: Gunnar
"""

def analyze_tickers( tickers, save_csv = True, period = "1y", interval = "1d", analysis_type = "d2d", plot_ticker = True ):
    
    return_df = pd.DataFrame( )
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        try:
            # Download historical data
            data = yf.download(ticker, period = period, interval = interval)
            data.index.name = 'Date'
            
            if analysis_type == "d2d":
                key_d2d = 'return_d2d'
                data[ key_d2d ] = data['Close'].pct_change() * 100
                return_df = pd.concat( [ return_df, data[ key_d2d ] ], axis = 1 )
                return_df = return_df.rename({ key_d2d: ticker }, axis='columns')
            if analysis_type == "d":
                key_d = 'return_d'
                data[ key_d ] = ( ( data['Close'] - data['Open'] ) / data['Open'] ) * 100
                return_df = pd.concat( [ return_df, data[ key_d ] ], axis = 1 )
                return_df = return_df.rename({ key_d: ticker }, axis='columns')
                

            if data.empty:
                print(f"No data found for {ticker}. Skipping.")
                continue

            
            if plot_ticker:
                
                __plot_tickers( data = data, ticker = ticker, period = period )
        
        except Exception as e:
            print(f"An error occurred for {ticker}: {e}")
            
    return_df.index.names = [ "Date" ] 
        
    if save_csv:
        csv_filename = "data/return_d.csv"
        return_df.to_csv(csv_filename)
        print(f"Saved data with day over day returns for S&P500 to {csv_filename}")
        
    return return_df