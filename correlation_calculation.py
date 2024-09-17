# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:59:34 2024

@author: Gunnar
"""

import pandas as pd

def compute_lagged_correlations(df, lag=0):
    tickers = df.columns
    lagged_corrs = pd.DataFrame(index=tickers, columns=tickers)

    df_shifted = df.shift(lag)

    lagged_corrs = df.corrwith(df_shifted, axis=0)

    return lagged_corrs


def compute_all_lagged_correlations(df, lag=0):
    
    tickers = df.columns
    corr_matrix = pd.DataFrame(index=tickers, columns=tickers)

    df_shifted = df.shift(lag)

    for ticker in tickers:
        corr_series = df.corrwith(df_shifted[ticker]) # df_shifted[ticker] = how stock performed on previous day
        corr_matrix[ticker] = corr_series # impact of ticker from prev day (if leg > 0)
        # for each column [ticker] rows show how column ticker - lag days impacts row ticker

    return corr_matrix
