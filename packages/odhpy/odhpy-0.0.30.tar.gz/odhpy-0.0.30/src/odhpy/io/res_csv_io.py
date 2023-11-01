import os
import numpy as np
import pandas as pd
from odhpy import utils



def read_res_csv(filename, custom_na_values=None, df=None, colprefix="", **kwargs):
    """Reads a res csv data file into a DataFrame, and sets the index to the Date.

    Args:
        filename (_type_): _description_
        custom_na_values (_type_): A list of values to override the automatically-determined missing values. If None, the missing values will include any defined in the .res.csv file as well as ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan'].

    Returns:
        _type_: _description_
    """
    # Handle custom na values
    if custom_na_values is None:
        na_values = ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan']
    else:
        na_values = custom_na_values
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # Scrape through the header
    metadata_lines = []
    eoh_found = False
    with open(filename) as f:
        line = ""
        for line in f:
            metadata_lines.append(line)
            if line.strip().startswith("EOH"):
                eoh_found = True
                break
            if custom_na_values is None and line.strip().lower().startswith("missing data value,"):
                new_na_value = line.strip()[len("missing data value,"):] #e.g. "-9999"
                na_values.append(new_na_value)
    if not eoh_found:
        return None #maybe it's not a .res.csv
    col_header_line_number = len(metadata_lines) - 2
    lines_to_skip = [i for i in range(col_header_line_number)] + [col_header_line_number + 1]
    # Read the data
    temp = pd.read_csv(filename, na_values=na_values, skiprows=lines_to_skip)
    temp = utils.set_index_dt(temp, dayfirst=True, format=r"%Y-%m-%d")    
    temp.index.name = 'Date'
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    if colprefix is not None:
        for c in temp.columns:
            temp.rename(columns = {c:f"{colprefix}{c}"}, inplace = True)        
    df = df.join(temp, how="outer").sort_index()
    utils.assert_df_format_standards(df)
    return df
