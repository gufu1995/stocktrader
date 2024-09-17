# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:45:02 2024

@author: Gunnar
"""
import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np
import requests
from lxml import html
import re

def gather_ticker_data( tickers, period = "1y", interval = "1d" ):
    
    collection_df = pd.DataFrame( )
    datetime_string = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    
    for ticker in tickers:
        
        print(f"Fetching data for {ticker}...")
        try:
            # Download historical data
            data_df = yf.download( ticker, period = period, interval = interval )
            
            if data_df.empty:
                print(f"No data found for {ticker}. Skipping.")
                continue
            
            data_df.index.name = 'Date'
            
            # calculate return for timeframe in percent
            key = 'returns_d'
            data_df[ key ] = data_df[ 'Close' ].pct_change() * 100
            
            # save ticker data to csv in ticker folder
            csv_ticker_name = f"data/ticker/{ticker}_{period}_{interval}.csv"
            data_df.to_csv(csv_ticker_name)
            print(f"Saved data with day over day returns for {ticker} to {csv_ticker_name}")
            
            collection_df = pd.concat( [ collection_df, data_df[ key ] ], axis = 1 )
            collection_df = collection_df.rename({ key: ticker }, axis = 'columns' )
        
        except Exception as e:
            print(f"An error occurred for {ticker}: {e}")
            
    collection_df.index.names = [ "Date" ] 
    collection_df = collection_df.astype( np.float32 )
    collection_df.index = pd.to_datetime(collection_df.index)
    collection_df = collection_df.dropna(axis=0, how='all')
    
    if len( collection_df ) != 0:
        csv_filename = f"data/collection/returns_{interval}_{period}_{len(collection_df.columns)}_tickers_{datetime_string}.csv"
        collection_df.to_csv(csv_filename)
        print(f"Saved data with day over day returns for {len(collection_df)}_tickers to {csv_filename}")
    else: 
        print( "Collected List is empty" )
        
    return 


def load_data( filepath ):
    
    data_df = pd.read_csv( filepath )
    if 'Date' in data_df.columns:
        data_df = data_df.set_index( 'Date' )
        
    data_df = data_df.astype( np.float32 )
    
    data_df.index = pd.to_datetime(data_df.index)
    data_df = data_df.dropna(axis=0, how='all')
    
    return data_df

def update_ticker_file( filepath, period, interval, ticker ):
    
    data_df = load_data( filepath )
    data_df = data_df.sort_index()
    data_df[ "returns_d" ] = data_df[ 'Close' ].pct_change() * 100
    csv_ticker_name = f"data/ticker/{ticker}_{period}_{interval}.csv"
    
    
    data_df.to_csv(csv_ticker_name)
    print(f"Saved data with day over day returns for {ticker} to {csv_ticker_name}")
    
    return data_df

def clean_data( data_df, start_date, end_date, zero_threshold = 0.1 ):
    
    if ( start_date > data_df.index[ 0 ] ) & ( end_date < data_df.index[ -1 ] ):
        
        data_df = data_df[ ( data_df.index > start_date ) & ( data_df.index < end_date ) ]
        
    missing_values = data_df.isnull().sum( axis = 0 )
    threshold = int(0.1 * len(data_df))  # For example, drop stocks with more than 10% missing data
    
    stocks_to_drop = missing_values[missing_values > threshold].index
    
    data_df = data_df.drop(columns=stocks_to_drop)
    
    return data_df

def get_sp500_csv( ):

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_df = tables[0]
    sp500_df = sp500_df.set_index( "Symbol" )
    sp500_df = sp500_df.rename( columns = { "Security" : "Description", "GICS Sector" : "Sector" } )
    sp500_df = sp500_df.loc[ :, [ "Description", "Sector" ] ]
    sp500_df.index.name = "Ticker"
    csv_name = "data/ticker_collection/sp500.csv"
    sp500_df.to_csv(csv_name)
    print(f"Saved ticker list for sp500 to {csv_name}")
    
    return 

def data_retreival_routine( period = "max", interval = "1d" ):
    
    tickers = get_sp500_csv()

    gather_ticker_data( tickers = tickers, period = period, interval = interval )
    
    return

def extract_ticker_description(symbol_str):
    # Split at the first space to separate ticker and description
    parts = symbol_str.strip().split(' ', 1)
    ticker = parts[0]
    description_with_date = parts[1] if len(parts) > 1 else ''
    
    # Regular expression to remove the date at the end
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s-]*\d{0,4}$'
    description = re.sub(date_pattern, '', description_with_date).strip()
    
    # Remove any trailing commas or hyphens
    description = description.rstrip(',-')
    
    return pd.Series({'Ticker': ticker, 'Description': description})

def get_commodities_csv( ):
    url = 'https://finance.yahoo.com/markets/commodities/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    tables = pd.read_html(response.content)
    print(f"Number of tables extracted: {len(tables)}")
    
    commodities_df = tables[0]
    commodities_df[['Ticker', 'Description']] = commodities_df['Symbol'].apply(extract_ticker_description)
    
    commodities_df = commodities_df.set_index(  "Ticker" )
    commodities_df = commodities_df.loc[ :, [ "Description" ] ]
    commodities_df.index.name = "Ticker"
    
    csv_name = "data/ticker_collection/commodities.csv"
    commodities_df.to_csv(csv_name)
    print(f"Saved ticker list for commodities to {csv_name}")
    
    return 

def load_ticker_data( filepath ):
    
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"The file '{filepath}' was not found.")
        return None