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
        
    #print([i['job id'] for i in selected_rows])
    return ("Selected Jobs: "+str([i['job id'] for i in selected_rows]))

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

power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P'}
def get_unit(alist):
    hi = max(alist)
    from math import log
    #print(alist)
    return power_labels[int(log(hi,1024))]
def convtounit(val,reqUnit):
    # Letter to Unit reverse search
    unitp = list(power_labels.keys())[list(power_labels.values()).index(reqUnit)]
    return val/1024**unitp

nclick = 0

@app.callback(
    [Output('table-multicol-sorting', 'data'),
    Output('table-multicol-sorting', 'columns'),
    Output(component_id='content2', component_property='children')],
    [Input('raw-switch', 'value'),
    Input('new-data-button', 'n_clicks'),
    Input(component_id='searchdf', component_property='value')])
def update_output(raw_toggle, new_data, search_value):
    from layouts import df
    ctx = dash.callback_context
    # CTX Needs to be used... 
    logger.info("{}{}{}".format(ctx.triggered,ctx.inputs,ctx.states))
    # Here nclick tracks how many times new data is pressed
    # this is used to update if it has changed
    global nclick

    # New Data button clicked
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
        #logger.debug("Orig: cpu_time {} type:{}".format(orig.iloc[[0]]['cpu_time'],type(orig.iloc[[0]]['cpu_time'])))
        alt = orig.copy()
        #logger.debug("Alt: cpu_time {} type:{}".format(alt.iloc[[0]]['cpu_time'],type(alt.iloc[[0]]['cpu_time'])))
    else:
        orig = df
        alt = orig.copy()
    ctx = dash.callback_context
    #logger.info(value)
    
    # If Raw toggle is switched
    # Convert usertime to percentage
    if not raw_toggle:
        alt['usertime'] = alt['usertime'] / orig['cpu_time']
        alt['usertime'] = pd.Series(
            [float("{0:.2f}".format(val * 100)) for val in alt['usertime']], index=alt.index)
        alt['systemtime'] = alt['systemtime'] / orig['cpu_time']
        alt['systemtime'] = pd.Series(
            [float("{0:.2f}".format(val * 100)) for val in alt['systemtime']], index=alt.index)
        alt.rename(columns={
            'systemtime': 'systemtime (%cpu_time)',
            'usertime': 'usertime (%cpu_time)',
        }, inplace=True)

    # Convert Bytes
        in_units = alt['bytes_in'].tolist()
        in_units = get_unit(in_units)
        out_units = alt['bytes_out'].tolist()
        out_units = get_unit(out_units)
        logger.info("Input units {}b Output Units {}b".format(in_units,out_units))
        alt['bytes_in'] = alt['bytes_in'].apply(convtounit,reqUnit=in_units).round(1)#.map('{:.2f}'.format)
        alt['bytes_out'] = alt['bytes_out'].apply(convtounit,reqUnit=out_units).round(1)#.map('{:.2f}'.format)
        alt.rename(columns={
            'bytes_in': 'bytes_in ({}b)'.format(in_units),
            'bytes_out': 'bytes_out ({}b)'.format(out_units),
        }, inplace=True)

    # Convert durations
        alt['duration (HH:MM:SS)'] = pd.to_timedelta(alt['duration (HH:MM:SS)'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['duration (HH:MM:SS)'] = pd.to_datetime(alt['duration (HH:MM:SS)'], format="%H:%M:%S").dt.time
        alt['cpu_time'] = pd.to_timedelta(alt['cpu_time'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['cpu_time'] = pd.to_datetime(alt['cpu_time'], format="%H:%M:%S").dt.time
        alt.rename(columns={'cpu_time':'cpu_time (HH:MM:SS)'}, inplace=True)

    # Run the search
    query = []
    algebra = ["==","=",">","<"]
    if any(n in search_value for n in algebra): # Handle incomplete search
        for item in search_value.split(","): # Break query into subqueries
            for al in algebra:
                if len(item.split(al)) >= 2 and item.split(al)[1] is not '': # Setup equal searches
                    logger.debug("{}{}".format(al,item.split(al)))
                    query.append([al,item.split(al)])
        try:
            for q in query:
                # Fuzzy
                if q[0] == '=':
                    alt = alt.loc[alt[q[1][0]].str.contains(q[1][1])]
                if q[0] == '==':
                    logger.debug("Checking for exact {} {}".format(q[1][0],q[1][1]))
                    alt = alt.loc[alt[q[1][0]] == q[1][1]]
                if q[0] == '>':
                    alt = alt.loc[alt[q[1][0]] > int(q[1][1])]
                if q[0] == '<':
                    alt = alt.loc[alt[q[1][0]] < q[1][1]]
        except Exception as e:
            logger.error("Threw exception on query: {}".format(e))
    return [
        alt.to_dict('records'),
        [{"name": i, "id": i} for i in alt.columns],
        'You\'ve entered: {}'.format(query)
    ]

######################## /Index Callbacks ######################## 



