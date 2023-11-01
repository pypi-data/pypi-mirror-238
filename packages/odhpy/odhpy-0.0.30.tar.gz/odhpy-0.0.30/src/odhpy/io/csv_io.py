import os
import numpy as np
import pandas as pd
from odhpy import utils
na_values = ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan']



def read_ts_csv(filename, date_format=None, df=None, colprefix="", **kwargs):
    """Reads a daily timeseries csv into a DataFrame, and sets the index to the Date.
    Assumed there is a column named "Date"

    Args:
        filename (_type_): _description_
        date_format (str, optional): defaults to "%d/%m/%Y" as per Fors. Other common formats include "%Y-%m-%d", "%Y/%m/%d".

    Returns:
        _type_: _description_
    """
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # Read the data
    temp = pd.read_csv(filename, na_values=na_values, **kwargs)
    temp = utils.set_index_dt(temp, dayfirst=True, format=date_format)    
    temp.index.name = 'Date'
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    if colprefix is not None:
        for c in temp.columns:
            temp.rename(columns = {c:f"{colprefix}{c}"}, inplace = True)        
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    # TODO: I SHOULD MAKE DEFAULT BEHAVIOUR AUTO-DETECT FORMAT DEPENDING ON *TYPE* AND *LOCATION* OF DELIMIT CHARS
    # TODO: In the meantime we use the below to assert that the format of the resulting df meets our minimum standards.
    utils.assert_df_format_standards(df)
    return df



def write_ts_csv(df: pd.DataFrame, filename: str):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        filename (str): _description_
    """
    df.to_csv(filename)