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

# 
@app.callback(dash.dependencies.Output('content', 'data'),
              [dash.dependencies.Input('test', 'children')])
def display_page(pathname):
    #import layouts
    logger.debug("Pathname is {}".format(pathname))
    import jobs
    joblist = jobs.job_gen()
    df = joblist.df
    return df.to_dict('records')


# Callback for reference model table updating
# Input: 
#   create new model button click
#   delete model button click
# State: 
#   recent jobs table selected and data
# Output:
#   text area on recent jobs screen
#   reference model table
#
# Output: 
from refs import make_refs
@app.callback(
    [dash.dependencies.Output('recent-job-model-status', 'children'),
    dash.dependencies.Output('table-ref-models','data')],
    [dash.dependencies.Input('create-newModel-btn', 'n_clicks_timestamp'),
    dash.dependencies.Input('delete-Model-btn', 'n_clicks_timestamp')],
    [dash.dependencies.State('table-multicol-sorting', 'selected_rows'),
    dash.dependencies.State('table-multicol-sorting', 'data'),
    dash.dependencies.State('table-ref-models', 'selected_rows'),
    dash.dependencies.State('table-ref-models', 'data')
    
    ])
def update_output(new_model_btn,delete_model_btn, sel_jobs,job_data,sel_refs,ref_data):

    # Create model on selected rows
    selected_rows = []
    from layouts import ref_df
    if int(new_model_btn) > int(delete_model_btn):
        if sel_jobs:
            selected_rows=[job_data[i]['job id'] for i in sel_jobs]
            logger.debug("Selected jobs {}".format(selected_rows))
            # Generate new refs for each of selected jobs
            import pandas as pd
            refa = make_refs(1,name='t')
            refa = pd.DataFrame(refa, columns=['Model','Tags','Jobs','Features','Active'])
            logger.info("ref_df before append id({})".format(id(ref_df)))
            ref_df = ref_df.append({'Jobs':selected_rows,'Tags':{'test':'tag'}},ignore_index=True)
            logger.info("ref_df after append id({})".format(id(ref_df)))
            from json import dumps
            ref_df['Tags'] = ref_df['Tags'].apply(dumps)
            logger.debug("Updating Refs with \n{}".format(ref_df))
            logger.debug(repr(ref_df))
            return [selected_rows, ref_df.to_dict('records')]
        return ["None selected", ref_df.to_dict('records')]
    # Delete Model
    elif int(new_model_btn) < int(delete_model_btn):
        if sel_refs:
            selected_refs=[ref_data[i]['Model'] for i in sel_refs]
            logger.info("Ref is {}".format(selected_refs))
            return [selected_rows, ref_df.to_dict('records')]
    else:
        return [selected_rows, ref_df.to_dict('records')]

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

from components import convtounit, get_unit, power_labels

# Global click counter hack to track button click changes in single instance
nclick = 0

# Callback:
# inputs:
#   raw-switch - the toggle for converting datatypes
#   new-data-button - a button for resetting the random jobs
#   searchdf - a text area that actively is run on keypress

# outputs:
#   table, data - This is the data in the main jobs table
#   table, columns - The table column names can be changed
#   content2 - This text area displays the search inputs interpretation of a query
@app.callback(
    [Output('table-multicol-sorting', 'data'),
    Output('table-multicol-sorting', 'columns'),
    Output(component_id='content2', component_property='children')],
    [Input('raw-switch', 'value'),
    Input('new-data-button', 'n_clicks'),
    Input(component_id='searchdf', component_property='value'),
    Input(component_id='jobs-date-picker', component_property='start_date'),
    Input(component_id='jobs-date-picker', component_property='end_date')])
def update_output(raw_toggle, new_data, search_value,start,end):
    logger.info("Update_output started")
    from layouts import df
    # Limit by time
    if end:
        from datetime import datetime, timedelta
        logger.info("Comparing start day {} with input {}".format(type(df['start_day']), datetime.strptime(start, "%Y-%m-%d").date() ))
        mask = (df['start_day'] > datetime.strptime(start, "%Y-%m-%d").date() - timedelta(days=1)) & (df['start_day'] <= datetime.strptime(end, "%Y-%m-%d").date())
        logger.debug("{} {}".format(start,end))
        df = df.loc[mask]
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
        alt['bytes_in'] = alt['bytes_in'].apply(convtounit,reqUnit=in_units).round(2)#.map('{:.2f}'.format)
        alt['bytes_out'] = alt['bytes_out'].apply(convtounit,reqUnit=out_units).round(2)#.map('{:.2f}'.format)
        alt.rename(columns={
            'bytes_in': 'bytes_in ({}b)'.format(in_units),
            'bytes_out': 'bytes_out ({}b)'.format(out_units),
        }, inplace=True)

    # Convert durations
        alt['duration'] = pd.to_timedelta(alt['duration'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['duration'] = pd.to_datetime(alt['duration'], format="%H:%M:%S").dt.time
        alt['cpu_time'] = pd.to_timedelta(alt['cpu_time'], unit='us').apply(lambda x: x*10000).apply(strfdelta)
        alt['cpu_time'] = pd.to_datetime(alt['cpu_time'], format="%H:%M:%S").dt.time
        alt.rename(columns={'cpu_time':'cpu_time (HH:MM:SS)','duration':'duration (HH:MM:SS)'}, inplace=True)

    # Run the search
    query = []
    separator = ","
    equalities = ["==","=",">","<"]
    if any(n in search_value for n in equalities): # Wait for user to enter comparison symbol
        # Take user input into a query list
        for item in search_value.split(separator): # Break query into subqueries on a sep
            for al in equalities:
                if len(item.split(al)) >= 2 and item.split(al)[1] is not '': # Setup equal searches
                    #logger.debug("Comparison '{}' on Values:{}".format(al,item.split(al)))
                    query.append([al,item.split(al)])
        # Attempt to parse queries
        try:
            # Q[0] is Query Equality Type
            # Q[1][0] is Column to search on
            # Q[1][1] is Value to check column for
            # Example:
            # query = [['=', ['processing complete', 'Y']],]
            for q in query:
                logger.debug("Processing Query: {}".format(q))
                logger.debug("Datatype is {}".format(alt[q[1][0]].dtype))
                # Fuzzy
                if q[0] == '=':
                    logger.debug("Checking for fuzzy '{}' '{}'".format(q[1][0],q[1][1]))
                    # Should probably check if alt[q[1][0]] is string
                    # Here I use np.object as a string comparison
                    if alt[q[1][0]].dtype == np.object:
                        alt = alt.loc[alt[q[1][0]].str.contains(q[1][1])]
                    # If Searching on a integer column convert second param to int
                    elif alt[q[1][0]].dtype == np.int64:
                        alt = alt.loc[alt[q[1][0]] == int(q[1][1])]
                    else:
                        alt = alt.loc[alt[q[1][0]].str.contains(str(q[1][1]))]
                if q[0] == '==':
                    logger.debug("Checking for exact '{}' '{}'".format(q[1][0],q[1][1]))
                    # If Searching on a integer column convert second param to int
                    if alt[q[1][0]].dtype == np.int64:
                        alt = alt.loc[alt[q[1][0]] == int(q[1][1])]
                    else:
                        alt = alt.loc[alt[q[1][0]] == q[1][1]]
                    
                
                if q[0] == '>':
                    from components import conv_str_time
                    if ':' in q[1][1]:
                        t = conv_str_time(q[1][1])
                        alt = alt.loc[alt[q[1][0]] > t]
                    else:
                        alt = alt.loc[alt[q[1][0]] > int(q[1][1])]

                if q[0] == '<':
                    from components import conv_str_time
                    if ':' in q[1][1]:
                        t = conv_str_time(q[1][1])
                        alt = alt.loc[alt[q[1][0]] > t]
                    else:
                        alt = alt.loc[alt[q[1][0]] < int(q[1][1])]
                logger.debug("DF has {} rows. \nFirst 5:\n{}".format(alt.shape[0],alt.head(5)))
            #logger.debug("The Query column is\n{}".format(alt[q[1][0]]))
        except Exception as e:
            logger.error("Threw exception on \nquery: ({})\nexception: ({})".format(q,e))
    logger.info("Update_output complete")
    return [
        alt.to_dict('records'),
        [{"name": i, "id": i} for i in alt.columns],
        'You\'ve entered: {}'.format(query)
    ]

######################## /Index Callbacks ######################## 

######################## Create Ref Callback ######################## 



######################## /Create Ref Callbacks ######################## 
