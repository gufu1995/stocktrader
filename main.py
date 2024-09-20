# -- coding: utf-8 --
"""
Created on Tue Sep 17 11:23:16 2024

@author: fuchsg1
"""


import pandas as pd
import data_retreival as dr
# import correlation_calculation as cc




start_date = pd.to_datetime("2020-09-11 00:00:00")
end_date = pd.to_datetime("2024-09-14 00:00:00")
folderpath = "data/ticker/"
data_format = "D"
interpolate = "linear"
stock_exchanges = [ "NYSE" ]

collect_df = dr.DATA_COLLECT_local_data( folderpath = folderpath, desired_date_format = data_format, start_date = start_date, 
                          end_date = end_date, exchanges = stock_exchanges, interpolate = interpolate )





# dr.data_retreival_routine( period = "max", interval = "1d" )
# dr.get_commodities_csv()
# dr.get_sp500_csv()



# sp500_filepath = "data/collection/returns_1d_max_501_tickers_2024-09-17_18-07-20.csv"
# sp500_df = dr.load_data( filepath = sp500_filepath )



# sp500_trimmed_df = dr.clean_data( data_df = sp500_df, start_date = start_date, end_date = end_date, zero_threshold = 0.1 )

# sp500_corr_lag = cc.compute_all_lagged_correlations( df = sp500_trimmed_df, lag = 1 )


# sp500_tickers = dr.load_ticker_data( "data/ticker_collection/sp500.csv" )
# commodity_tickers = dr.load_ticker_data( "data/ticker_collection/commodities.csv" )
# smi_tickers = dr.load_ticker_data( "data/ticker_collection/smi.csv" )


# urn_df = dr.update_ticker_file( "data/ticker/URN_D.csv", period = "max", interval = "1d", ticker = "URN" )

# milk = yf.download( "SIL=F", period = "1y", interval = "1d" )











# lag = 1

# lagged_corr_matrix = compute_all_lagged_correlations(data, lag=lag)

# lagged_corr_flat = lagged_corr_matrix.unstack().dropna()
# threshold = 0.2  

# significant_pairs = lagged_corr_flat[lagged_corr_flat.abs() > threshold] # Impact of index 1 lagging by lag days on index 2
# significant_pairs_sorted = significant_pairs.sort_values(ascending=False)


# plt.figure(figsize=(14, 14))
# sns.heatmap(lagged_corr_matrix.astype(float), cmap='coolwarm', center=0, annot=False)
# plt.title(f'Lagged Correlation Matrix at Lag {lag} Days')
# plt.xlabel('Stocks')
# plt.ylabel('Stocks')
# plt.show()



# high_corr_pairs = high_corr_pairs.stack().sort_values( )

# high_corr_pairs = high_corr_pairs[high_corr_pairs > 0.8]