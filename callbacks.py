import dash
from dash.dependencies import Input, Output, State
from app import app
import plotly.graph_objs as go
from plotly import tools

from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime

import numpy as np
import pandas as pd

import io


#from components import formatter_currency, formatter_currency_with_cents, formatter_percent, formatter_percent_2_digits, formatter_number
#from components import update_first_datatable, update_first_download, update_second_datatable, update_graph

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

#pd.options.mode.chained_assignment = None

######################## Select rows Callbacks ######################## 

@app.callback(
    Output('content','children'),
    [Input('table-multicol-sorting', 'data'),
    Input('table-multicol-sorting', 'selected_rows')])
def f(data,rows):
    selected_rows = []
    if rows:
        selected_rows=[data[i] for i in rows]
            #or
            #selected_rows=pd.DataFrame(rows).iloc[i] 
        
    print([i['Job ID'] for i in selected_rows])
    return ("Selected Rows: "+str([i['Job ID'] for i in selected_rows]))

# Custom Select all
# This callback 
# https://community.plot.ly/t/data-table-select-all-rows/16619/2
# Input:
#       n_clicks is used to trigger this callback
# State:
#       The data is used to count the rows
#       The selected rows is used to determine if all or none should be
#            selected
# Output:
#       The datatable selected_rows will be updated
@app.callback(
    Output('table-multicol-sorting', "selected_rows"),
    [Input('index-select-all', 'n_clicks'),],
    [State('table-multicol-sorting',"data"),
    State('table-multicol-sorting', "selected_rows")]
)
def select_all(n_clicks,data,selected_count):
    if selected_count:
        # If All rows selected
        if len(data) == len(selected_count):
            # Deselect all
            return []
    return [i for i in range(len(data))]

def format_bytes(size,roundn=2):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return (str(round(size,roundn)) + power_labels[n]+'B')

def strfdelta(tdelta, fmt="{hours}:{minutes}:{seconds}"):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

nclick = 0

@app.callback(
    [Output('table-multicol-sorting', 'data'),
    Output('table-multicol-sorting','columns')],
    [Input('my-toggle-switch', 'value'),
    Input('new-data-button', 'n_clicks')])
def update_output(value,new_data):
    from layouts import df
    # Here nclick tracks how many times new data is pressed
    # this is used to update if it has changed
    global nclick

    # If new data is pressed once or more than once
    if new_data is not nclick:
        # Update global with click count
        logger.debug("New Data pressed")
        nclick = new_data
        
        # Reset class instance with new random jobs
        import jobs
        new_jobs= jobs.job_gen()
        new_jobs.reset()
        # Set new random jobs as original
        orig = new_jobs.df
        # Check original against alternative df
        logger.debug("Orig: cpu_time {} type:{}".format(orig.iloc[[0]]['cpu_time'],type(orig.iloc[[0]]['cpu_time'])))
        alt = orig.copy()
        logger.debug("Alt: cpu_time {} type:{}".format(alt.iloc[[0]]['cpu_time'],type(alt.iloc[[0]]['cpu_time'])))
    else:
        logger.debug("New Data not pressed")
        orig = df
        alt = orig.copy()
    ctx = dash.callback_context
    logger.info(value)
    
    # Convert usertime to percentage
    if value:
        alt['usertime'] = alt['usertime'] / orig['cpu_time']
        alt['usertime'] = pd.Series(
            ["{0:.2f}%".format(val * 100) for val in alt['usertime']], index=alt.index)
        alt['systemtime'] = alt['systemtime'] / orig['cpu_time']
        alt['systemtime'] = pd.Series(
            ["{0:.2f}%".format(val * 100) for val in alt['systemtime']], index=alt.index)
        alt.rename(columns={
            'systemtime': 'systemtime (% of cpu_time)',
            'usertime': 'usertime (% of cpu_time)',
        }, inplace=True)

    # Convert Bytes
    if value:
        alt['bytes_in'] = alt['bytes_in'].apply(format_bytes)
        alt['bytes_out'] = alt['bytes_out'].apply(format_bytes)
    
    # Convert Durations
    if value:
        alt['duration'] = pd.to_timedelta(alt['duration'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['duration'] = pd.to_datetime(alt['duration'], format="%H:%M:%S").dt.time
        alt['cpu_time'] = pd.to_timedelta(alt['cpu_time'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['cpu_time'] = pd.to_datetime(alt['cpu_time'], format="%H:%M:%S").dt.time

    logger.info("cpu_time {} type:{}".format(orig.iloc[[0]]['cpu_time'],type(orig.iloc[[0]]['cpu_time'])))
    logger.info("cpu_time {} type:{}".format(alt.iloc[[0]]['cpu_time'],type(alt.iloc[[0]]['cpu_time'])))

    return [alt.head(10).to_dict('records'),
    [{"name": i, "id": i} for i in sorted(alt.columns)]
    ]

######################## /Index Callbacks ######################## 



