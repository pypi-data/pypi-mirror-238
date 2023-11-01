import pandas as pd
import altair as alt
import numpy as np
from typing import Union
from odhpy import utils
from odhpy import io
from odhpy import trans
import calendar
from datetime import datetime, timedelta

def wy_event_heatmap(df=Union[pd.DataFrame,pd.Series],criteria=1,y_title="Series",pass_label="Pass",fail_label="Fail",pass_colour="white",fail_colour="red",width=None,height=None,stroke='black',strokeWidth=0.3):
    """Returns an Altair heatmap chart from a timeseries input of event count by Water Year.

    Args:
        df (DataFrame | Series): Annual (WY) index timeseries of no. of 'events' in a year i.e. output of StorageLevelAssessment.AnnualDaysBelowSummary()
        criteria (int, optional): Minimum integer in df that triggers a 'failure'. Defaults to 1.
        y_title (str, optional): Y axis title. Defaults to "Series".
        pass_label (str, optional): Label for years that don't meet the criteria. Defaults to "Pass".
        fail_label (str, optional): Label for years that meet the criteria. Defaults to "Fail".
        pass_colour (str, optional): Colour for years that don't meet the criteria. Defaults to "white".
        fail_colour (str, optional): Colour for years that meet the criteria. Defaults to "red".
        width (int, optional): Width of chart output. Defaults to None.
        height (int, optional): Height of chart output. Defaults to None.
        stroke (str, optional): Colour of rectangle outline. Defaults to black.
        strokeWidth (float, optional): Width of rectangle outline. Defaults to 0.3.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    # If df input is a Series, first convert to DataFrame
    if type(df) is pd.Series:
        df=pd.DataFrame(df)

    # df column names must be str for Altair
    df.columns=[str(x) for x in df.columns]
    columns=df.columns.values


    # Lookup table to convert count of events by WY to 'pass' or 'fail
    lookup = pd.DataFrame({
    'key': ['1', '0'],
    'y': [fail_label,pass_label]
    })

    domain = [pass_label, fail_label]
    range = [pass_colour, fail_colour]

    # Altair needs vega expression. Generate based on criteria input
    vega_expr_str = 'if(datum.value>=' + str(criteria) + ',1,0)'

    # Default width and height expression
    if width == None:
        width = df.shape[0]*10
    if height == None:
        height = len(columns)*25
    
    chart_wy_event = alt.Chart(df.reset_index() # Reset index so that Altair can access Date index
    ).transform_fold( # Fold individual columns into single column
        columns,
        as_=['column','value']
    ).transform_calculate( # Convert count of WY events to 1 or 0 based on criteria
        value=vega_expr_str
    ).transform_lookup( # Convert 1 and 0 to pass and fail
        lookup='value',
        from_=alt.LookupData(lookup, key='key', fields=['y'])
    ).mark_rect(stroke=stroke, strokeWidth=strokeWidth
    ).encode(
        alt.X('index:O', title='Water Year'),
        alt.Y('column:N',sort=None, title=y_title),
        color=alt.Color('y:N', scale=alt.Scale(domain=domain,range=range), title="Key")
    ).properties(
        width=width,
        height=height
    )

    return chart_wy_event

def pyblo(dflist: list, sites: list, series: list, wy_month=1, site_order=None, series_order=None, colours=None, start_date=None, end_date=None, series_label="Series", site_label=None, label_freq=10, subtitle=True, width=None, height=35, stroke_width=0.5, stroke_colour='black',font_size=12, grid_colour='lightgrey'):
    """Returns a chart depicting available data by Water Year. Data is arranged by site with colour assigned by series. 

    Args:
        dflist (list): List of pd.Series data.
        sites (list): List of strings by which corresponding data in dflist is grouped by chart row.
        series (list): List of strings by which corresponding data in dflist is grouped by colour.
        wy_month (int, optional): Water year start month. Defaults to 1.
        site_order (list, optional): Optional order to arrange Sites by. Defaults to order in sites.
        series_order (list, optional): Optional order to arrange Series by. Defaults to order in series.
        colours (list, optional): Optional list of colours (arranged by series_order) to apply to Series. Defaults to selection from "muted rainbow" colour scheme.
        start_date (DateTime, optional): Optional minimum date (%d/%m/%Y) to display. Defaults to None.
        end_date (DateTime, optional): Optional maximum date (%d/%m/%Y) to display. Defaults to None.
        series_label (str, optional): Optional Series label for legend. Defaults to "Series".
        site_label (str, optional): Optional Site y-axis title. Defaults to None.
        label_freq (int, optional): Optional frequency to display year label. Defaults to 10 (years).
        subtitle (bool, optional): Whether to show subtitle. Defaults to True.
        width (int, optional): Optional chart width parameter. Defaults to function of total years.
        height (int, optional): Optional chart height parameter. Represents height per facet/site. Defaults to 35.
        stroke_width (float, optional): Optional width of bar outline. Defaults to 0.5.
        stroke_colour (str, optional): Optional colour of bar outline. Defaults to 'black'.
        font_size (int, optional): Optional font size to apply to all text. Defaults to 12.
        grid_colour (str, optional): Optional colour of gridlines. Defaults to 'lightgrey'.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    # Check that inputs are the same length
    if len(set([len(dflist),len(sites),len(series)])) != 1:
        raise Exception("All input lists must be of the same length")
    
    # Check that dflist is a list of pd.Series
    if (set([type(x) for x in dflist]) != {pd.Series}) or (set([type(x.index) for x in dflist]) != {pd.DatetimeIndex}):
        raise Exception("All dflist entries must be a single column of a datetime-indexed dataframe (pd.Series)")  

    ## Initialise inputs
    using_end_year=False ## README: Assume False for Chas' get_wy commit

    ## Month lookup
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]  

    # Get list of sites from first element of input dict   
    sitelist_unique = pd.unique(sites)   # list of unique sites to plot

    # Get list of series from second element of input dict
    serieslist_unique = pd.unique(series)   # list of unique series to plot

    # If colours array not provided, assign default colour scheme
    if colours == None:
        colours = ["#72AC57", "#639188", "#5C77B0", "#765EA4", "#98467A", "#BA3438", "#CF512B", "#E18433"]  # muted rainbow
    
    # If order array not provided, assign default order
    if series_order == None:
        series_order = serieslist_unique

    if site_order == None:
        site_order = sitelist_unique

    # Generate Vega expression for x-axis label frequency
    label_expr="year(datum.value) % " + str(label_freq) + " ? null : datum.label"

    # Rename data series columns for Altair folding
    [x.rename('Series'+str(i),inplace=True) for i,x in enumerate(dflist)]
    columnlist=[x.name for x in dflist]

    # Combine all data into single df
    df_chart=pd.concat(dflist,axis=1)

    # Get WY count of data
    df_chart_annual = df_chart.groupby(utils.get_wy(df_chart.index,wy_month,using_end_year=using_end_year)).count()

    # Calculate number of days in the WY
    if using_end_year:
        if wy_month>2:
            df_chart_annual["Day_count"]=[366 if calendar.isleap(x) else 365 for x in df_chart_annual.index.values]
        else:
            df_chart_annual["Day_count"]=[366 if calendar.isleap(x-1) else 365 for x in df_chart_annual.index.values]
    else:
        if wy_month>2:
            df_chart_annual["Day_count"]=[366 if calendar.isleap(x+1) else 365 for x in df_chart_annual.index.values]
        else:
            df_chart_annual["Day_count"]=[366 if calendar.isleap(x) else 365 for x in df_chart_annual.index.values]        

    # Convert count of data to percentage of year
    df_chart_annual_perc=df_chart_annual.divide(df_chart_annual["Day_count"].values, axis=0)

    # Reset index to DateTime instead of integer
    df_chart_annual_perc.index = [pd.Timestamp(x,1,1) for x in df_chart_annual_perc.index.to_list()]

    # Lookup table to assign site from data input name (df column)
    lookup = pd.DataFrame({
        'key': columnlist,
        'r': sites
    })

    # Lookup table to assign series from data input name (df column)
    lookup_colour = pd.DataFrame({
        'key': columnlist,
        'c': series
    })

    # Default domain expression
    end_date_year=df_chart_annual_perc.index[-1].year

    if start_date == None:
        start_date = df_chart_annual_perc.index[0]
    else:
        start_date_wy=utils.get_wy(utils.get_dates(pd.to_datetime(start_date,dayfirst=True),days=1),wy_month)[0]
        start_date = pd.Timestamp(start_date_wy,1,1)
    if end_date == None:
        end_date = df_chart_annual_perc.index[-1].replace(year=end_date_year+1)
    else:
        end_date_wy=utils.get_wy(utils.get_dates(pd.to_datetime(end_date,dayfirst=True),days=1),wy_month)[0]
        end_date = pd.Timestamp(end_date_wy+1,1,1)


    # Default width and height expression
    no_years = end_date.year-start_date.year+1
    if width == None:
        width = no_years*12       

    # Show subtitle if parameter is True
    if subtitle:    
        subtitle = ["Annual (" + months[wy_month-1] + " to " + months[wy_month-2] + ") percentage of available data: " + format(start_date.replace(month=wy_month),"%d/%m/%Y") + " - " + format(end_date.replace(month=wy_month)-timedelta(1),"%d/%m/%Y")]
    else:
        subtitle=[]

    chart=alt.Chart(df_chart_annual_perc.reset_index()
    ).transform_fold( # Fold wide-format df to long-format
        columnlist,
        as_=['columns','values']
    ).transform_lookup( # Lookup data column site
        lookup='columns',
        from_=alt.LookupData(lookup, key='key', fields=['r'])
    ).transform_lookup( # Lookup data column series
        lookup='columns',
        from_=alt.LookupData(lookup_colour, key='key', fields=['c'])
    ).mark_bar(
        width=alt.RelativeBandSize(1),
        clip=True
    ).encode(
        x=alt.X(
            'index:T',
            timeUnit='year',
            axis=alt.Axis(
                ticks=False,
                tickCount=999999,
                orient='top',
                labelAngle=90,
                title=None,
                grid=True,
                gridColor=grid_colour,
                labelPadding=5,
                labelExpr=label_expr),
            scale=alt.Scale(domain=[start_date,end_date])),
        y=alt.Y(
            'values:Q',
            title=None,
            axis=alt.Axis(
                format=".1%",
                tickCount=0)).stack(None),
        strokeWidth=alt.condition('datum.values > 0',alt.value(stroke_width),alt.value(0)), # don't show tiny bars for years with no data
        stroke=alt.value(stroke_colour),
        color=alt.Color('c:N',
            sort=series_order,
            title=series_label,
            scale=alt.Scale(range=colours)),
        order=alt.Order('color_c_sort_index:Q'),
        tooltip=[
            alt.Tooltip(
                'values:Q',
                format='.1%',
                title="Percentage"),
                alt.Tooltip(
                    'c:N',
                    title=series_label),
                alt.Tooltip(
                    'index:T',
                    title="Water Year",
                    format='%Y')],
        row=alt.Row(
            field='r',
            sort=site_order,
            spacing=0,
            title=site_label,
            header=alt.Header(
                labelAngle=0,
                labelAlign='left',
                labelOrient='left'))
    ).properties(
        height=height,
        width=width,
        title=alt.TitleParams(
            subtitle,
            baseline='bottom',
            orient='bottom',
            anchor='start',
            fontWeight='normal',
            fontStyle='italic',
            fontSize=font_size*0.9,
            offset=font_size*0.9*2)
    ).configure_view(
        stroke='black'
    ).configure_axis(
        labelFontSize=font_size,
        titleFontSize=font_size
    ).configure_headerRow(
        labelFontSize=font_size,
        titleFontSize=font_size 
    ).configure_legend(
        labelFontSize=font_size,
        titleFontSize=font_size 
    )
    
    return chart

def exceedence_plot(df:pd.DataFrame,yLabel='Flow (ML/d)',xLog=False,yLog=False,legendTitle='Data set',plotWidth=500,plotHeight=300,plottingPosition="cunnane"):
    """
    Exceedance plot of timeseries data.

    Args:
        df (pd.DataFrame): Dataframe of daily timeseries data.
        yLabel (str, optional): Y axis title. Defaults to 'Flow (ML/d)'.
        xLog (bool, optional): X axis log flag. Defaults to False.
        yLog (bool, optional): Y axis log flag. Defaults to False.
        legendTitle (str, optional): Legend title. Defaults to 'Data set'.
        plotWidth (int, optional): Chart width. Defaults to 500.
        plotHeight (int, optional): Chart height. Defaults to 300.
        plottingPosition (str, optional): Defaults to "cunnane". Other supported values: "weibull", "gringorten". See https://glossary.ametsoc.org/wiki/Plotting_position

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    df_exceedence = df.dropna()
    nn = len(df_exceedence)
    df_exceedence["Exceedence"] = trans.get_exceedence_plotting_position(nn,plotting_position=plottingPosition)
    df_exceedence.set_index("Exceedence", inplace=True)

    for i in range(len(df_exceedence.columns)):
        col = df_exceedence.columns[i]
        lab = col
        df_exceedence[col] = df_exceedence[col].sort_values(ascending=False).values
    
    if xLog:
        xType="log"
    else:
        xType="linear"

    if yLog:
        yType="log"
    else:
        yType="linear"

    df_exc_melted = df_exceedence.reset_index().melt('Exceedence')
    df_exc_melted.rename(columns={'value':yLabel,'variable':legendTitle}, inplace=True)
    excPlot=alt.Chart(df_exc_melted).mark_line().encode(
        alt.X('Exceedence:Q',
          axis=alt.Axis(title='Exceedance probability (%)')).scale(type=xType),
        alt.Y(yLabel + ':Q',
          axis=alt.Axis(title=yLabel)).scale(type=yType),
        color=legendTitle,
        tooltip=[alt.Tooltip('Exceedence',format=',.1f',title='Exceedence (%)'),alt.Tooltip(yLabel,format=',.0f')]
    ).properties(width=plotWidth,height=plotHeight).interactive(bind_y=False)
    
    return excPlot


def daily_plot(df:pd.DataFrame,yLabel='Flow (ML/d)',legendTitle='Data set',plotWidth=500,plotHeight=300):
    """
    Daily plot of timeseries data.

    Args:
        df (DataFrame): Dataframe of daily timeseries data.
        yLabel (str, optional): Y axis title. Defaults to 'Flow (ML/d)'.
        legendTitle (str, optional): Legend title. Defaults to 'Data set'.
        plotWidth (int, optional): Chart width. Defaults to 500.
        plotHeight (int, optional): Chart height. Defaults to 300.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    alt.data_transformers.disable_max_rows()

    df_melted = df.reset_index().melt('Date')
    df_melted.rename(columns={'value':yLabel,'variable':legendTitle}, inplace=True)
    dailyPlot=alt.Chart(df_melted).mark_line().encode(
        alt.X('Date:T',
          axis=alt.Axis(title='Date')),
        alt.Y(yLabel + ':Q',
          axis=alt.Axis(title=yLabel)),
        color=legendTitle,
        tooltip=[alt.Tooltip(legendTitle),alt.Tooltip('Date',title='Date'),alt.Tooltip(yLabel,format=',.0f')]
    ).properties(width=plotWidth,height=plotHeight).interactive(bind_y=False)
    
    return dailyPlot


def annual_plot(df:pd.DataFrame,yLabel='Flow (ML/a)',legendTitle='Data set',wyStartMonth=7,plotWidth=500,plotHeight=300):
    """
    Annual plot of timeseries data.

    Args:
        df (DataFrame): Dataframe of daily timeseries data.
        yLabel (str, optional): Y axis title. Defaults to 'Flow (ML/a)'.
        legendTitle (str, optional): Legend title. Defaults to 'Data set'.
        wyStartMonth (int, optional): Water year start month. Defaults to 7.
        plotWidth (int, optional): Chart width. Defaults to 500.
        plotHeight (int, optional): Chart height. Defaults to 300.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    alt.data_transformers.disable_max_rows()
    xLabel='Water year'

    if wyStartMonth==1: xLabel='Water year (Jan to Dec)'
    if wyStartMonth==2: xLabel='Water year (Feb to Jan)'
    if wyStartMonth==3: xLabel='Water year (Mar to Feb)'
    if wyStartMonth==4: xLabel='Water year (Apr to Mar)'
    if wyStartMonth==5: xLabel='Water year (May to Apr)'
    if wyStartMonth==6: xLabel='Water year (Jun to May)'
    if wyStartMonth==7: xLabel='Water year (Jul to Jun)'
    if wyStartMonth==8: xLabel='Water year (Aug to Jul)'
    if wyStartMonth==9: xLabel='Water year (Sep to Aug)'
    if wyStartMonth==10: xLabel='Water year (Oct to Sep)'
    if wyStartMonth==11: xLabel='Water year (Nov to Oct)'
    if wyStartMonth==12: xLabel='Water year (Dec to Nov)'

    start_date=utils.get_wy_start_date(df,wyStartMonth)
    end_date=utils.get_wy_end_date(df,wyStartMonth) + timedelta(days=1) #Add day because last index in .loc is not included
    cropped_df=df.loc[utils.get_dates(start_date,end_date)]
    annual_cropped_df=cropped_df.groupby(utils.get_wy(cropped_df.index, wyStartMonth)).sum(min_count=365)

    df_melted = annual_cropped_df.reset_index().melt('index')
    df_melted.rename(columns={'index':'Water year','value':yLabel,'variable':legendTitle}, inplace=True)
    annualPlot=alt.Chart(df_melted).mark_line().encode(
        alt.X('Water year',
          axis=alt.Axis(title=xLabel,format='.0f')),
        alt.Y(yLabel + ':Q',
          axis=alt.Axis(title=yLabel)),
        color=legendTitle,
        tooltip=[alt.Tooltip(legendTitle),alt.Tooltip('Water year'),alt.Tooltip(yLabel,format=',.0f')]
    ).properties(width=plotWidth,height=plotHeight).interactive(bind_y=False)
    
    return annualPlot

def residual_mass_curve(df:pd.DataFrame,yLabel='Flow residual mass (ML)',legendTitle='Data set',plotWidth=500,plotHeight=300):
    """
    Residual mass curve of timeseries data.

    Args:
        df (DataFrame): Dataframe of daily timeseries data.
        yLabel (str, optional): Y axis title. Defaults to 'Flow residual mass (ML)'.
        legendTitle (str, optional): Legend title. Defaults to 'Data set'.
        plotWidth (int, optional): Chart width. Defaults to 500.
        plotHeight (int, optional): Chart height. Defaults to 300.

    Returns:
        altair.Chart: Returns an Altair chart object
    """

    alt.data_transformers.disable_max_rows()

    residualMass=df.copy()
    
    for i in range (0,len(df.columns)):
        col=df.columns[i]
        avg=df[col].mean()
        cumDiff=0
        tempResidMass=[]
        for j in range (0,len(residualMass)):
            if(pd.isna(residualMass[col][j])):
                tempResidMass.append(float("nan"))
            else:
                todayDiff=residualMass[col][j]-avg
                cumDiff+=todayDiff
                tempResidMass.append(cumDiff)
        residualMass[col + ' residual mass']=tempResidMass
        residualMass.drop(columns=[col],inplace=True)

    df_melted = residualMass.reset_index().melt('Date')
    df_melted.rename(columns={'value':yLabel,'variable':legendTitle}, inplace=True)
    residMassPlot=alt.Chart(df_melted).mark_line().encode(
        alt.X('Date:T',
          axis=alt.Axis(title='Date')),
        alt.Y(yLabel + ':Q',
          axis=alt.Axis(title=yLabel)),
        color=legendTitle,
        tooltip=[alt.Tooltip(legendTitle),alt.Tooltip('Date',title='Date'),alt.Tooltip(yLabel,format=',.0f')]
    ).properties(width=plotWidth,height=plotHeight).interactive(bind_y=False)
    
    return residMassPlot