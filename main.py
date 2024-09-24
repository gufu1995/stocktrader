# -- coding: utf-8 --
"""
Created on Tue Sep 17 11:23:16 2024

@author: fuchsg1
"""


import pandas as pd
import data_retreival as dr
import analysis as az
import os
# import correlation_calculation as cc

start_date = pd.to_datetime("2011-01-01 00:00:00")
end_date = pd.to_datetime("2024-08-01 00:00:00")
ticker_data_folderpath = "data/ticker/commodities/"
ticker_collection_folderpath = "data/ticker_collection/"
data_collection_folderpath = "data/ticker/stocks/"
data_format = "M"
period = "max"
interval = f"1{ 'mo' if data_format.lower() == 'm' else data_format.lower()}"
interpolate = "linear"
stock_exchanges = [ "NYSE", "NASDAQ" ]

# local_df = dr.DATA_COLLECT_local_data( folderpath = ticker_data_folderpath, desired_date_format = data_format, start_date = start_date, 
#                           end_date = end_date, exchanges = stock_exchanges, interpolate = interpolate )
# dr.LOCAL_safe_to_csv( data = local_df, filepath = "data/returns/local_M.csv" )
# ticker_df = dr.META_get_ticker_df( folder_path = ticker_collection_folderpath )
# dr.LOCAL_safe_to_csv(data = ticker_df, filepath = ticker_collection_folderpath + "ticker_df.csv" )
# new_ticker_df = dr.LOCAL_load_csv_data( ticker_collection_folderpath + "ticker_df.csv" )
# returns_df = dr.DL_fetch_Yahoo_ticker_data( tickers = new_ticker_df.index, period = period, interval = interval, exchanges = stock_exchanges,
#                               folder = data_collection_folderpath, start_date = start_date, end_date = end_date,
#                               interpolate = "linear", fill_missing = False )
# dr.LOCAL_safe_to_csv( data = returns_df, filepath = f"data/returns/returns_{data_format}.csv" )
# local_df = dr.LOCAL_load_csv_data(filepath = f"data/returns/local_{data_format}.csv" )
# returns_df = dr.LOCAL_load_csv_data(filepath = f"data/returns/returns_{data_format}.csv" )

# data = dr.DATA_merge_dataframes(dfs = [ returns_df, local_df ], threshold=1e-8)
# dr.LOCAL_safe_to_csv( data = data, filepath = f"data/returns/returns_cpl_{data_format}.csv" )

commodities_files = "data/ticker/commodities/"
commodities_files = [ commodities_files + f for f in os.listdir(commodities_files) if os.path.isfile(os.path.join(commodities_files, f))]
commodities_filtered = [ _ for _ in commodities_files if _.split("_")[-1][ 0 ] == "M" ]
# az.EXECUTE_fn_filelist( filelist = commodities_files, function = az.ANALYSE_file )

stock_files = "data/ticker/stocks/"
stock_files = [ stock_files + f for f in os.listdir(stock_files) if os.path.isfile(os.path.join(stock_files, f))]
az.EXECUTE_fn_filelist( filelist = stock_files, function = az.ANALYSE_file )

# returns_df = dr.LOCAL_load_csv_data(filepath = f"data/returns/returns_cpl_{data_format}.csv" )
# ticker_data = dr.LOCAL_load_csv_data( filepath = "data/ticker/commodities/ALUM_M.csv" )
# ticker_time_trimmed = dr.DATA_FILTER_complete_csv_data_time( data_series = ticker_data, 
#                                                             start_date = start_date, end_date= end_date )
# az.plot_complete_data(ticker = "ALUM", data = ticker_time_trimmed, safe = True, filepath = "charts/stocks/" )

