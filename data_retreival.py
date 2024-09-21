# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:45:02 2024

@author: Gunnar
"""
import yfinance as yf
import pandas as pd
import datetime 
import numpy as np
import requests
import re
import pandas_market_calendars as mcal
import os 

def META_stock_exchange_tickers( ):
    tickers = ['ASX', 'BMF', 'B3', 'BSE', 'NSE', 'XNSE', 'CFE', 'CBOE_Futures', 
               'CBOE_Equity_Options', 'CBOE_Index_Options', 'CME_Equity', 'CBOT_Equity', 
               'CME_Agriculture', 'CBOT_Agriculture', 'COMEX_Agriculture', 'NYMEX_Agriculture', 
               'CME_Rate', 'CBOT_Rate', 'CME_InterestRate', 'CBOT_InterestRate', 'CME_Bond', 'CBOT_Bond', 
               'CMEGlobex_Livestock', 'CMEGlobex_Live_Cattle', 'CMEGlobex_Feeder_Cattle', 'CMEGlobex_Lean_Hog', 
               'CMEGlobex_Port_Cutout', 'CME Globex Cryptocurrencies', 'CME Globex Crypto', 'CMEGlobex_EnergyAndMetals', 
               'CMEGlobex_Energy', 'CMEGlobex_CrudeAndRefined', 'CMEGlobex_NYHarbor', 'CMEGlobex_HO', 'HO', 
               'CMEGlobex_Crude', 'CMEGlobex_CL', 'CL', 'CMEGlobex_Gas', 'CMEGlobex_RB', 'RB', 'CMEGlobex_MicroCrude', 
               'CMEGlobex_MCL', 'MCL', 'CMEGlobex_NatGas', 'CMEGlobex_NG', 'NG', 'CMEGlobex_Dutch_NatGas', 'CMEGlobex_TTF', 
               'TTF', 'CMEGlobex_LastDay_NatGas', 'CMEGlobex_NN', 'NN', 'CMEGlobex_CarbonOffset', 'CMEGlobex_CGO', 
               'CGO', 'C-GEO', 'CMEGlobex_NGO', 'NGO', 'CMEGlobex_GEO', 'GEO', 'CMEGlobex_Metals', 
               'CMEGlobex_PreciousMetals', 'CMEGlobex_Gold', 'CMEGlobex_GC', 'GC', 'CMEGlobex_Silver', 
               'CMEGlobex_SI', 'SI', 'CMEGlobex_Platinum', 'CMEGlobex_PL', 'PL', 'CMEGlobex_BaseMetals', 
               'CMEGlobex_Copper', 'CMEGlobex_HG', 'HG', 'CMEGlobex_Aluminum', 'CMEGlobex_ALI', 'ALI', 'CMEGlobex_QC', 
               'QC', 'CMEGlobex_FerrousMetals', 'CMEGlobex_HRC', 'HRC', 'CMEGlobex_BUS', 'BUS', 'CMEGlobex_TIO', 'TIO', 
               'CME Globex Equity', 'CMEGlobex_FX', 'CME_FX', 'CME_Currency', 'CME Globex Fixed Income', 
               'CME Globex Interest Rate Products', 'EUREX', 'EUREX_Bond', 'HKEX', 'ICE', 'ICEUS', 'NYFE', 'NYSE', 
               'stock', 'NASDAQ', 'BATS', 'DJIA', 'DOW', 'IEX', 'Investors_Exchange', 'JPX', 'XJPX', 'LSE', 'OSE', 
               'SIFMAUS', 'SIFMA_US', 'Capital_Markets_US', 'Financial_Markets_US', 'Bond_Markets_US', 'SIFMAUK', 
               'SIFMA_UK', 'Capital_Markets_UK', 'Financial_Markets_UK', 'Bond_Markets_UK', 'SIFMAJP', 'SIFMA_JP', 
               'Capital_Markets_JP', 'Financial_Markets_JP', 'Bond_Markets_JP', 'SIX', 'SSE', 'TASE', 'TSX', 'TSXV', 
               'TradingCalendar', 'AIXK', 'ASEX', 'BVMF', 'CMES', 'IEPA', 'XAMS', 'XASX', 'XBKK', 'XBOG', 'XBOM', 'XBRU', 
               'XBSE', 'XBUD', 'XBUE', 'XCBF', 'XCSE', 'XDUB', 'XDUS', 'XEEE', 'XFRA', 'XETR', 'XHAM', 'XHEL', 'XHKG', 
               'XICE', 'XIDX', 'XIST', 'XJSE', 'XKAR', 'XKLS', 'XKRX', 'XLIM', 'XLIS', 'XLON', 'XMAD', 'XMEX', 'XMIL', 
               'XMOS', 'XNYS', 'XNZE', 'XOSL', 'XPAR', 'XPHS', 'XPRA', 'XSAU', 'XSES', 'XSGO', 'XSHG', 'XSTO', 'XSWX', 
               'XTAE', 'XTAI', 'XTKS', 'XTSE', 'XWAR', 'XWBO', 'us_futures', '24/7', '24/5']
    
    for i, ticker in enumerate( tickers ):
        print( i, ": ", ticker )
    while True:
        try:
            number = int( input( "Which ticker to return?" ) )
            break
        except:
            print( "Not a number, try again" )
            
    return tickers[ number ]
        

def META_ANALYZE_local_filename( filename ):
    if "/" in filename:
        filename = filename.split("/")[ - 1 ]
    filename = filename.split( "." )[ 0 ]
    filename = filename.split( "_" )
    ticker = filename[ 0 ]
    date_format = filename[ -1 ]
    
    return ticker, date_format 


def META_extract_ticker_description(symbol_str):
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


def META_get_valid_trading_days( date_format, exchanges, start_date, end_date ):
    
    if date_format == "D":
        if exchanges == "None":
            valid_trading_dates = pd.date_range(start=start_date, end=end_date, freq="B" )
        else:
            if isinstance(exchanges, str):
                exchanges = [ exchanges ]

            for i, exchange in enumerate( exchanges ): 
                stock_exchange = mcal.get_calendar( exchange )
                valid_trading_dates_exchange = stock_exchange.valid_days(start_date=start_date, end_date=end_date)
                valid_trading_dates_exchange = pd.to_datetime( valid_trading_dates_exchange ).tz_localize(None)
                if i == 0:
                    valid_trading_dates = valid_trading_dates_exchange
                else:
                    valid_trading_dates = valid_trading_dates.union( valid_trading_dates_exchange )
        
    else:       
        if date_format == "MO":
            date_format = "MS"
        valid_trading_dates = pd.date_range(start=start_date, end=end_date, freq=date_format )
        
    return valid_trading_dates


def META_strip_non_trading_days( data_series, valid_trading_dates ):
    # if there are too many trading days in data, take the dates and shift them to the next trading day
    # then delete the none trading days
    excessive_dates = data_series.index.difference( pd.Index( valid_trading_dates ) )
    missing_dates = pd.Index( valid_trading_dates ).difference( data_series.index )
    
    for excessive_date in excessive_dates:
        next_valid_date = valid_trading_dates[valid_trading_dates > excessive_date].min()
        if pd.notna(next_valid_date):
            
            if next_valid_date in data_series.index:
            # Add the value from the non-trading day to the next valid day
                data_series.loc[next_valid_date] += data_series.loc[excessive_date]
            else:
            # If the next valid day has no value, assign the value directly
                data_series[next_valid_date] = data_series.loc[excessive_date]
                missing_dates = missing_dates.drop( next_valid_date )
            
            # data_df.loc[next_valid_date] = data_df.loc[next_valid_date].fillna(0) + data_df.loc[excessive_date]
    data_series = data_series.drop(index=excessive_dates)
    
    return data_series, missing_dates


def META_get_ticker_df( folder_path ):
    
    sp500df = DL_GATHER_sp500_tickers( folderpath = folder_path, safe_data = False )
    commodities_df = DL_GATHER_commodities_tickers( folderpath = folder_path, safe_data = False )
    qqq_df = LOCAL_load_csv_data( folder_path + "QQQ.csv" )
    smi_df = LOCAL_load_csv_data( folder_path + "smi.csv" )
    dax_df = LOCAL_load_csv_data( folder_path + "dax.csv" )

    ticker_df = [ sp500df, commodities_df, qqq_df, smi_df, dax_df ]
    ticker_df = DATA_COLLECT_ticker_list( ticker_df = ticker_df )
    
    return ticker_df


def DL_fetch_single_ticker_data( ticker, period, interval ):
    
    print(f"Fetching data for {ticker}...")
    try:

        ticker_df = yf.download( ticker, period = period, interval = interval )
        
        ticker_df.index.name = 'Date'

        ticker_df[ 'returns' ] = ticker_df[ 'Close' ].pct_change() * 100
        
        return ticker_df

    except Exception as e:
        print( f"An error occurred for {ticker}: {e}" )
        return None
        

def DL_fetch_Yahoo_ticker_data( tickers, start_date, end_date, exchanges, period = "1y", 
                               interval = "1d", folder = "data/ticker/stocks/", interpolate = "linear",
                               fill_missing = True):
    
    # if len(end_date)==0:
    #     end_date = pd.to_datetime( datetime.date.today( ) )
    #     if "y" in period:
    #         start_date = datetime.date.today() - datetime.timedelta( days = 365 + int( period[ : -1 ] ) )
    #     elif "d" in period:
    #         start_date = datetime.date.today() - datetime.timedelta( days = int( period[ : -1 ] ) )
    #     elif "w" in period:
    #         start_date = datetime.date.today() - datetime.timedelta( weeks = int( period[ : -1 ] ) )
    #     else:
    #         print( "Do not recognize the period" )
    #     start_date = pd.to_datetime( start_date )
            
    collection_df = pd.DataFrame( )
    datetime_string = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    
    valid_trading_dates = META_get_valid_trading_days( date_format = re.findall( r"[a-zA-Z]+", interval )[ 0 ].upper(), exchanges = exchanges, 
                                                     start_date = start_date, end_date = end_date )

    for ticker in tickers:

        ticker_df = DL_fetch_single_ticker_data( ticker = ticker, period = period, interval = interval )
        # save ticker data to csv in ticker folder
        csv_ticker_filepath = folder + f"{ticker}_{period}_{interval}.csv"
        LOCAL_safe_to_csv(data = ticker_df, filepath = csv_ticker_filepath )
        
        if ticker_df.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue
        
        ticker_series = ticker_df[ "returns" ]
        ticker_df_time_filtered = DATA_FILTER_complete_csv_data_time( data_series = ticker_series, start_date = start_date, end_date = end_date )
        
        try:
            missing_dates, returns_time_adjusted = DATA_ANALYZE_data_integrity( data_series = ticker_df_time_filtered, 
                                                                     exchanges = exchanges, start_date = start_date, valid_trading_dates = valid_trading_dates,
                                                                     end_date = end_date, calculate_trading_dates = False  )
            
            returns_timecomplete_series = DATA_MANIPULATE_fill_missing_data( data_series = returns_time_adjusted, fill = fill_missing,
                                                missing_dates = missing_dates, interpolate = interpolate )
            
            
            
    
            collection_df = pd.concat( [ collection_df, returns_timecomplete_series ], axis = 1 )
            collection_df = collection_df.rename({ 'returns': ticker }, axis = 'columns' )
        except Exception as e:
            print( e )
            continue
            
    collection_df.index.names = [ "Date" ] 
    collection_df = collection_df.astype( np.float32 )
    collection_df.index = pd.to_datetime(collection_df.index)
    collection_df = collection_df.dropna(axis=0, how='all')
    
    if len( collection_df ) != 0:
        csv_filename = folder +  f"returns_{interval}_{period}_{len(collection_df.columns)}_tickers_{datetime_string}.csv"
        collection_df.to_csv(csv_filename)
        print(f"Saved data with day over day returns for {len(collection_df)}_tickers to {csv_filename}")
    else: 
        print( "Collected List is empty" )
        
    return collection_df


def DL_GATHER_sp500_tickers( folderpath = "data/ticker_collection/", safe_data = False ):

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_df = tables[0]
    sp500_df = sp500_df.set_index( "Symbol" )
    sp500_df = sp500_df.rename( columns = { "Security" : "Description", "GICS Sector" : "Sector" } )
    sp500_df = sp500_df.loc[ :, [ "Description", "Sector" ] ]
    sp500_df.index.name = "Ticker"
    csv_name = folderpath + "sp500.csv"
    if safe_data:
        sp500_df.to_csv(csv_name)
        print(f"Saved ticker list for sp500 to {csv_name}")
    
    return sp500_df


def DL_GATHER_commodities_tickers( folderpath = "data/ticker_collection/", safe_data = False ):
    url = 'https://finance.yahoo.com/markets/commodities/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    tables = pd.read_html(response.content)
    print(f"Number of tables extracted: {len(tables)}")
    
    commodities_df = tables[0]
    commodities_df[['Ticker', 'Description']] = commodities_df['Symbol'].apply(META_extract_ticker_description)
    
    commodities_df = commodities_df.set_index(  "Ticker" )
    commodities_df = commodities_df.loc[ :, [ "Description" ] ]
    commodities_df.index.name = "Ticker"
    
    csv_name = "data/ticker_collection/commodities.csv"
    if safe_data:
        commodities_df.to_csv(csv_name)
        print(f"Saved ticker list for commodities to {csv_name}")
    
    return commodities_df


def LOCAL_load_csv_data( filepath ):
    
    data_df = pd.read_csv( filepath )
    
    if "Ticker" in data_df.columns:
        data_df = data_df.set_index( "Ticker" )
        data_df = data_df.dropna(axis=0, how='all')
        return data_df
    
    if 'Date' in data_df.columns:
        data_df = data_df.set_index( 'Date' )
        
    elif "Datum" in data_df.columns:
        data_df = data_df.set_index( 'Datum' )
        
    data_df = data_df.astype( np.float32 )
    data_df.index = pd.to_datetime(data_df.index )
    return data_df
        

def LOCAL_gather_folder_tickers( folderpath, desired_date_format ):
    file_collection = [ ]
    try:
        for file in os.listdir( folderpath ):
            if os.path.isfile(os.path.join(folderpath, file)):
                ticker, date_format = META_ANALYZE_local_filename( file )
                if date_format == desired_date_format:
                    file_collection.append( [ os.path.join(folderpath, file), ticker, date_format ] )
                else:
                    continue

        return file_collection
    except Exception as e:
        print( e )
        return None


def LOCAL_safe_to_csv( data, filepath ):

    data.to_csv(filepath)
    print(f"Saved data list for commodities to {filepath}")
    
    return


def DATA_EXTRACT_untouched_data_csv( data_df, ticker ):
    try:
        data_series = data_df.loc[ :, "returns" ]
        data_series = data_series.dropna(axis=0, how='all')
        data_series.name = ticker
        
    except Exception as e:
        print( e )
        return None
        
    return data_series


def DATA_FILTER_complete_csv_data_time( data_series, start_date, end_date ):
    
    if start_date > end_date:
        print( "Start Date is after End Date, switching the both" )
        start_date_copy = start_date.copy()
        start_date = end_date 
        end_date = start_date_copy
    elif start_date == end_date:
        print( "Start Date is equal to End Date - choose something else" )
        return None
    try:
        if ( start_date >= data_series.index[ 0 ] ) & ( end_date <= data_series.index[ -1 ] ):
        
            data_series = data_series[ ( data_series.index >= start_date ) & ( data_series.index <= end_date ) ]
            return data_series
        elif ( start_date >= data_series.index[ 0 ] ) & ( end_date > data_series.index[ -1 ] ):
            print( f"End Date {end_date} out of Scope, taking last element: {data_series.index[ -1 ]} instead")
            data_series = data_series[ ( data_series.index >= start_date ) ]
            return data_series 
        elif ( start_date < data_series.index[ 0 ] ) & ( end_date <= data_series.index[ -1 ] ):
            print( f"Start Date {start_date} out of Scope, taking first element: {data_series.index[ 0 ]} instead")
            data_series = data_series[ ( data_series.index <= end_date ) ]
            return data_series 
        else:
            print( "Start or End Date out of scope" )
            return data_series
    except Exception as e:
        print( e )
        return None
    
    
def DATA_ANALYZE_get_date_format( data_series ):
    
    date_diffs = data_series.index.to_series().diff().dropna()
    
    daily_diffs = (date_diffs == pd.Timedelta(days=1)).sum()
    weekly_diffs = (date_diffs == pd.Timedelta(weeks=1) ).sum()
    monthly_diffs = ((date_diffs >= pd.Timedelta(days=28)) & (date_diffs <= pd.Timedelta(days=32))).sum()  
    
    if daily_diffs > weekly_diffs and daily_diffs > monthly_diffs:
        print("The data primarily has daily intervals.")
        return "D"
    elif weekly_diffs > daily_diffs and weekly_diffs > monthly_diffs:
        print("The data primarily has weekly intervals.")
        return "W-SUN"
    elif monthly_diffs > daily_diffs and monthly_diffs > weekly_diffs:
        print("The data primarily has monthly intervals.")   
        return "MS"


def DATA_ANALYZE_data_integrity( data_series, exchanges, start_date, end_date, 
                                calculate_trading_dates = True, valid_trading_dates = None ):
    
    date_format = DATA_ANALYZE_get_date_format( data_series = data_series )

    if calculate_trading_dates:
        valid_trading_dates = META_get_valid_trading_days( date_format = date_format, 
                                                          exchanges = exchanges, start_date = start_date, 
                                                          end_date = end_date )
    
    data_series, missing_dates = META_strip_non_trading_days( data_series = data_series, 
                                                             valid_trading_dates = valid_trading_dates )

    if missing_dates.empty:
        print("The data is complete.")
    else:
        print("The data is missing for the following dates:")
        print(missing_dates)
        
    return missing_dates, data_series

    
def DATA_MANIPULATE_fill_missing_data( data_series, missing_dates, fill = True, interpolate = "linear" ):
    # interp values = 'linear', 'time', 'index', 'values', 'nearest', 'zero', 'slinear', 
    # 'quadratic', 'cubic', 'barycentric', 'krogh', 'spline', 'polynomial', 'from_derivatives', 
    #'piecewise_polynomial', 'pchip', 'akima', 'cubicspline'
    complete_series = data_series.reindex(data_series.index.union(missing_dates).sort_values())
    if fill:
        complete_series = complete_series.interpolate(method=interpolate)
        complete_series = complete_series.fillna( 0 )
    else: 
        complete_series = data_series 
    
    return complete_series
    

def DATA_MANIPULATE_clean_zeros( data_df, start_date, end_date, zero_threshold = 0.1 ):

    missing_values = data_df.isnull().sum( axis = 0 )
    threshold = int(0.1 * len(data_df))  # For example, drop stocks with more than 10% missing data
    
    stocks_to_drop = missing_values[missing_values > threshold].index
    
    data_df = data_df.drop(columns=stocks_to_drop)
    
    return data_df

 
def DATA_COLLECT_local_data( folderpath, desired_date_format, start_date, end_date, exchanges, interpolate ):
    
    local_tickers = LOCAL_gather_folder_tickers( folderpath = folderpath, desired_date_format = desired_date_format )

    for i, local_ticker in enumerate( local_tickers ):

        untouched_csv_ticker_data = LOCAL_load_csv_data( filepath = local_ticker[ 0 ] )
        extracted_returns_series = DATA_EXTRACT_untouched_data_csv( data_df = untouched_csv_ticker_data, 
                                                                   ticker = local_ticker[ 1 ] )


        returns_time_filtered = DATA_FILTER_complete_csv_data_time( data_series = extracted_returns_series, 
                                                                  start_date = start_date, end_date = end_date )
        missing_dates, returns_time_adjusted = DATA_ANALYZE_data_integrity( data_series = returns_time_filtered, 
                                                                 exchanges = exchanges, start_date = start_date, 
                                                                 end_date = end_date, calculate_trading_dates = True  )
        
        returns_timecomplete_series = DATA_MANIPULATE_fill_missing_data( data_series = returns_time_adjusted, fill = True,
                                            missing_dates = missing_dates, interpolate = interpolate )
        if i == 0:
            returns_collection_df = returns_timecomplete_series.to_frame( )
        else:
            returns_collection_df = pd.concat( [ returns_collection_df, returns_timecomplete_series.to_frame( ) ], axis = 1 )
        
    returns_collection_df.index.name = "Date"
    return returns_collection_df 

def DATA_COLLECT_ticker_list( ticker_df ):
    return pd.concat( ticker_df )


def DATA_check_duplicate_column_names(df):
    """
    Check for duplicate column names in a DataFrame.

    Parameters:
    - df: pandas DataFrame to check.

    Returns:
    - duplicates: list of duplicate column names.
    """
    counts = df.columns.value_counts()
    duplicates = counts[counts > 1].index.tolist()
    return duplicates


def DATA_merge_dataframes(dfs, threshold=1e-8):
    """
    Merge multiple DataFrames with datetime indexes and stock tickers as columns.

    Parameters:
    - dfs: list of pandas DataFrames to merge.
    - threshold: float, maximum allowed difference to consider data as similar.

    Returns:
    - merged_df: pandas DataFrame after merging.
    """
    # Check for duplicate column names in each DataFrame and handle them
    for idx, df in enumerate(dfs):
        duplicates = DATA_check_duplicate_column_names(df)
        if duplicates:
            print(f"Duplicate column names found in DataFrame {idx}: {duplicates}")

    # Start with the first DataFrame
    merged_df = dfs[0].copy()
    for df in dfs[1:]:
        # Find common columns
        common_cols = merged_df.columns.intersection(df.columns)
        for col in common_cols:
            df = df.drop(columns=[col])

        # Merge the DataFrames
        merged_df = pd.concat([merged_df, df], axis=1)
    return merged_df