import os
import numpy as np
import pandas as pd
from odhpy import utils
na_values = ['', ' ', 'null', 'NULL', 'NAN', 'NaN', 'nan', 'NA', 'na', 'N/A' 'n/a', '#N/A', '#NA', '-NaN', '-nan']



def read_iqqm_lqn_output(filename, col_name=None, df=None) -> pd.DataFrame:
    """Reads the output of IQQM listquan. This is format is the same for flows and diversions.

    Args:
        filename (_type_): _description_
        df (_type_, optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # If no column name was specified, we use the base name of the file
    if col_name is None:
        col_name = os.path.basename(filename)
    # Read the data
    data_start_row=7
    temp = pd.read_csv(filename, skiprows=(data_start_row-2), delim_whitespace=True, names=["Date", col_name], header=None)
    temp = utils.set_index_dt(temp, format='%d/%m/%Y')
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    # TODO: I SHOULD MAKE DEFAULT BEHAVIOUR AUTO-DETECT FORMAT DEPENDING ON *TYPE* AND *LOCATION* OF DELIMIT CHARS
    # TODO: In the meantime we use the below to assert that the format of the resulting df meets our minimum standards.
    utils.assert_df_format_standards(df)
    return df
    
    





