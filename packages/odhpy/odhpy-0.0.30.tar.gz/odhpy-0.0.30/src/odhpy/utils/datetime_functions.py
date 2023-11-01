from datetime import datetime, timedelta
import pandas as pd


def get_wy(dates, wy_month=7, using_end_year=False):
    """
    Returns water years, as a list of ints, for a given array of dates. Use this to
    add water year info into a pandas DataFrame. 

    The default (using_end_year=False) aligns water years with the primary water 
    allocation at the start of the water year. The alternative (using_end_year==True) 
    follows the convention used for fiscal years whereby water years are labelled 
    based on their end dates. Using the fiscal convention, the 2022 water year is 
    from 2021-07-01 to 2022-06-30 inclusive.
    """
    if using_end_year:
        answer = [d.year if d.month < wy_month else d.year + 1 for d in dates]
    else:
        answer = [d.year - 1 if d.month < wy_month else d.year for d in dates]        
    return answer


def get_dates(start_date, end_date=None, days=0, years=1, include_end_date=False):
    """
    Generates a list of daily datetime values from a given start date. The length 
    may be defined by an end_date, or a number of days, or a number of years. This 
    function may be useful for working with daily datasets and models.
    """
    if (days > 0):
        # great, we already have the number of days
        pass
    elif (end_date != None):
        # use end_date
        days = (end_date - start_date).days
        days = days + 1 if include_end_date else days
    else:
        # use years
        end_date = datetime(start_date.year + years, start_date.month, start_date.day,
            start_date.hour, start_date.minute, start_date.second, start_date.microsecond)
        days = (end_date - start_date).days
    date_list = [start_date + timedelta(days=x) for x in range(days)]
    return date_list

def get_wy_start_date(df:pd.DataFrame, wy_month=7):
    """
    Returns an appropriate water year start date based on data frame dates and the
    water year start month.

    Args:
        df (pd.DataFrame): Dataframe with date as index
        wy_month (int, optional): Water year start month. Defaults to 7.

    Returns:
        datetime: Water year start date.
    """
    first_date=df.index[0]
    first_day=first_date.day
    first_month=first_date.month
    first_year=first_date.year

    if (first_month<wy_month):
        #If month is less than wy_month we can start wy this year
        start_month=wy_month
        start_day=1
        start_year=first_year
    elif (first_month==wy_month):
        #If month equal to wy_month check that data starts on first day of month and set year accordingly
        if (first_day>1):
            start_month=wy_month
            start_day=1
            start_year=first_year+1
        else:
            start_month=wy_month
            start_day=1
            start_year=first_year
    else:
        #If month is greater than wy_month we have to start wy next year
        start_month=wy_month
        start_day=1
        start_year=first_year+1
    
    return datetime(start_year,start_month,start_day)

def get_wy_end_date(df:pd.DataFrame, wy_month=7):
    """
    Returns an appropriate water year end date based on data frame dates and the
    water year start month.

    Args:
        df (pd.DataFrame): Dataframe with date as index
        wy_month (int, optional): Water year start month. Defaults to 7.

    Returns:
        datetime: Water year end date.
    """
    last_date=df.index[(len(df) - 1)]
    last_day=last_date.day
    last_month=last_date.month
    last_year=last_date.year

    if (wy_month==1):
        wy_month_end=12
    else:
        wy_month_end=wy_month-1

    if wy_month_end in { 1, 3, 5, 7, 8, 10, 12 }:
        wy_day_end=31
    elif wy_month_end in { 4, 6, 9, 11 }:
        wy_day_end=30
    else:
        #Setting number of days in Feb to 28 - handle leap years at the end of this function
        wy_day_end=28

    if (last_month>wy_month_end):
        #If month is greater than wy_month_end we can start wy this year
        end_month=wy_month_end
        end_day=wy_day_end
        end_year=last_year
    elif (last_month==wy_month_end):
        #If month equal to wy_month_end check that data ends on last day of month and set year accordingly
        if (last_day<wy_day_end):
            end_month=wy_month_end
            end_day=wy_day_end
            end_year=last_year-1
        else:
            end_month=wy_month_end
            end_day=wy_day_end
            end_year=last_year
    else:
        #If month is less than wy_month_end we have to end wy last year
        end_month=wy_month_end
        end_day=wy_day_end
        end_year=last_year-1

    #This handles the February's that have 29 days
    if (end_month==2):
        end_day=(datetime(end_year,end_month+1,1) - timedelta(days=1)).day
    
    return datetime(end_year,end_month,end_day)