# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:13:30 2024

@author: fuchsg1
"""

from os import listdir
from os.path import isfile, join

import pandas as pd
import numpy as np

mypath = "data/ticker/backup/"
files = [ f for f in listdir(mypath) if isfile(join(mypath, f))]

def convert_to_float(val):
    if isinstance(val, str):
        return val.replace('.', '').replace(',', '.')
    return val


for file in files:
    
    Ticker = file.split( "_" )[ 0 ]
    Format = file.split( "_")[ 1 ].split( "." )[ 0 ]
    
    if Ticker != "NICKEL":
        if Format != "D":
            continue
    
    
    # print( file )
    
    data = pd.read_csv( mypath + file )
    if "Datum" in data.columns:
        
        data = data.set_index( "Datum" )
        try:
            data.index = pd.to_datetime( data.index, dayfirst = True )
            data = data.rename( columns = { "Zuletzt" : "Close", "Eröffn." : "Open", "Hoch" : "High", "Tief" : "Low" } )
            data.index.name = "Date"
        except Exception as e:
            print( e, Ticker )
        
    else:
        data = data.set_index( "Date" )
        try:
            data.index = pd.to_datetime( data.index, dayfirst = False )
            data = data.rename( columns = { "Price" : "Close" } )
        except Exception as e:
            print( e, Ticker )

    data = data.loc[ :, [ "High", "Low", "Open", "Close" ] ]
    data = data.sort_index()
    data = data.map(convert_to_float)
    data = data.astype( np.float32 )
    data[ "returns" ] = data[ 'Close' ].pct_change() * 100
    
    filepath = f"data/ticker/{Ticker}_{Format}.csv"
    
    data.to_csv( filepath )