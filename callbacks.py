import dash
from dash.dependencies import Input, Output, State
from app import app
import plotly.graph_objs as go
from plotly import tools
from datetime import datetime as dt
from datetime import date, timedelta
import io
from datetime import datetime
import numpy as np
import pandas as pd
# Index.py Configures logger debug level
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

# These are old example methods that were used by template..
#from components import formatter_currency, formatter_currency_with_cents, formatter_percent, formatter_percent_2_digits, formatter_number
#from components import update_first_datatable, update_first_download, update_second_datatable, update_graph

#pd.options.mode.chained_assignment = None
from layouts import DEFAULT_ROWS_PER_PAGE
from layouts import dcc
# 
@app.callback(dash.dependencies.Output('content', 'data'),
              [dash.dependencies.Input('test', 'children')])
def display_page(pathname):
    #import layouts
    logger.debug("Pathname is {}".format(pathname))
    from jobs import job_gen
    joblist = jobs.job_gen().df
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
@app.callback(
    [
        dash.dependencies.Output('recent-job-model-status', 'children'),
        dash.dependencies.Output('table-ref-models','data'),
        dash.dependencies.Output('edit-model-div','style'),
        #dash.dependencies.Output('table-multicol-sorting', 'selected_rows')
    ],
    [
        dash.dependencies.Input('create-newModel-btn', 'n_clicks_timestamp'),
        dash.dependencies.Input('delete-Model-btn', 'n_clicks_timestamp'),
        dash.dependencies.Input('toggle-Model-btn', 'n_clicks_timestamp'),
        dash.dependencies.Input('edit-Model-btn', 'n_clicks_timestamp'),
        dash.dependencies.Input('edit-Model-close-btn', 'n_clicks_timestamp'),
        dash.dependencies.Input('edit-Model-save-btn', 'n_clicks_timestamp')
    ],
    [
        dash.dependencies.State('table-multicol-sorting', 'selected_rows'),
        dash.dependencies.State('table-multicol-sorting', 'data'),
        dash.dependencies.State('table-ref-models', 'selected_rows'),
        dash.dependencies.State('table-ref-models', 'data')
    ])
def update_output(new_model_btn,delete_model_btn, toggle_model_btn, edit_model_btn, edit_model_close_btn, edit_model_save_btn, sel_jobs,job_data,sel_refs,ref_data):
    from datetime import datetime, timedelta
    current_time = (datetime.now()- timedelta(seconds=1)).timestamp()
    selected_rows = []
    import layouts
    ref_df = layouts.ref_df
    from components import recent_button
    recentbtn = recent_button(
        {'new_model':new_model_btn,
        'delete_model':delete_model_btn,
        'toggle_model':toggle_model_btn,
        'edit_model':edit_model_btn,
        'close_edit':edit_model_close_btn,
        'save_edit':edit_model_save_btn
        }
    )
    logger.debug("Recent click {}".format(recentbtn))
# Create model
    current_time = (datetime.now()- timedelta(seconds=1)).timestamp()
    if recentbtn is 'new_model':
        if sel_jobs:
            selected_rows=[str(job_data[i]['job id']) for i in sel_jobs]
            logger.info("Selected jobs {}".format(selected_rows))
            # Generate new refs for each of selected jobs
            import pandas as pd
            from json import dumps
            # Make_refs returns a list of 
            from refs import make_refs
            refa = make_refs(1,name='t',jobs=selected_rows)
            refa = pd.DataFrame(refa, columns=['name','date created','tags','jobs','features','active'])
            refa['jobs'] = refa['jobs'].apply(dumps)
            refa['tags'] = refa['tags'].apply(dumps)
            refa['features'] = refa['features'].apply(dumps)
            logger.info("Creating new model with \n{}".format(refa))
            layouts.ref_df = pd.concat([ref_df,refa], ignore_index=True, sort=False)
            #logger.info(repr(ref_df))
            return [selected_rows, layouts.ref_df.to_dict('records'),{'display':'none'}]
        return ["None selected", ref_df.to_dict('records'),{'display':'none'}]
    
# Delete Model
    if recentbtn is 'delete_model':
        if sel_refs and len(sel_refs)>0:
            selected_refs=[ref_data[i]['name'] for i in sel_refs]
            logger.info("Delete Model {}".format(selected_refs))
            for n in selected_refs:
                layouts.ref_df = ref_df[ref_df.name != n]
            return [selected_rows, layouts.ref_df.to_dict('records'),{'display':'none'}]
        return [selected_rows, ref_df.to_dict('records'),{'display':'none'}]
# Toggle Active Status
    if recentbtn is 'toggle_model':
        if sel_refs and len(sel_refs)>0:
            selected_refs = ref_data[sel_refs[0]]['name']
            logger.info("Toggle model name {} pre-invert active {}".format(selected_refs, ref_df[ref_df.name == selected_refs].active))
            # Where the 'name' is selected set 'active' as the np.invert of what it was
            layouts.ref_df.loc[(ref_df.name == selected_refs),'active'] = ~ref_df[ref_df.name == selected_refs].active
            logger.info("post-invert active {}".format(layouts.ref_df[ref_df.name == selected_refs].active ))
        return [selected_rows, ref_df.to_dict('records'),{'display':'none'}]
# Edit Model
    if recentbtn is 'edit_model':
        if sel_refs and len(sel_refs)>0:
            selected_refs = ref_data[sel_refs[0]]['name']
            return [selected_rows, layouts.ref_df.to_dict('records'),{'display':'contents'}]
# Save and Close edit model
    if recentbtn is 'save_edit':
        return [selected_rows, layouts.ref_df.to_dict('records'),{'display':'none'}]
# Close edit model
    if recentbtn is 'close_edit':
        return [selected_rows, layouts.ref_df.to_dict('records'),{'display':'none'}]
    return [selected_rows, ref_df.to_dict('records'),{'display':'none'}]
    

######################## Select rows Callbacks ######################## 
@app.callback(
    Output('content','children'),
    [
        Input('table-multicol-sorting', 'data'),
        Input('table-multicol-sorting', 'selected_rows'),
        #Input('table-multicol-sorting', '')
    ])
def f(data,selected_rows):
    selected_jobs = []
    if selected_rows:
        selected_jobs=[data[i] for i in selected_rows]
            #or
            #selected_rows=pd.DataFrame(rows).iloc[i] 
        
    #print([i['job id'] for i in selected_rows])
    return ("Selected Jobs: "+str([i['job id'] for i in selected_jobs]))

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


# Recent jobs data table callback
# inputs:
#   raw-switch - the toggle for converting datatypes
#   new-data-button - a button for resetting the random jobs
#   searchdf - a text area that actively is run on keypress
#   row-count-dropdown - Requested number of rows per page

# outputs:
#   table, data - This is the data in the main jobs table
#   table, columns - The table column names can be changed
#   content2 - This text area displays the search inputs interpretation of a query
@app.callback(
    [Output('table-multicol-sorting', 'data'),
     Output('table-multicol-sorting', 'columns'),
     Output(component_id='content2', component_property='children'),
     Output('page-selector', 'children'),
     Output('table-multicol-sorting', "page_size"),
     Output('table-multicol-sorting', "page_count")],
    [Input('raw-switch', 'value'),
     Input(component_id='searchdf', component_property='value'),
     Input(component_id='jobs-date-picker', component_property='start_date'),
     Input(component_id='jobs-date-picker', component_property='end_date'),
     Input(component_id='row-count-dropdown', component_property='value'), # Requested row limiter
     Input('table-multicol-sorting', "page_current"),  # Page Number - 1
     #Input('table-multicol-sorting', "page_size"),  # How many rows the table wants to have per page
     Input('table-multicol-sorting', "sort_by")  # What is requested to sort on
     ])
def update_output(raw_toggle, search_value, start, end, rows_per_page, page_current, sort_by):
    logger.info("Update_output started")
    ctx = dash.callback_context
    # Debug Context due to this callback being huge
    logger.debug("Callback Context info:\nTriggered:\n{}\nInputs: {}\nStates: {}\n".format(ctx.triggered,ctx.inputs,ctx.states))
    from jobs import job_gen
    logger.debug("Rows requested per page:{}".format(rows_per_page))
    offset = 0
    # Grab df
    job_df = job_gen().df
    # Sort
    if len(sort_by):
        job_df = job_df.sort_values(
            sort_by[0]['column_id'], # Column to sort on
            ascending=sort_by[0]['direction'] == 'asc', # Boolean eval.
            inplace=False
        )
    # /sort
    # Filter
    #####
    # Reduce
    len_jobs = int(job_df.shape[0])
    import layouts
    logger.debug(layouts.ref_df.loc[layouts.ref_df['name'] == 'ref0'].active)
    job_df = job_df.iloc[page_current*int(rows_per_page):(page_current+ 1)*int(rows_per_page)]
    # /Reduce
    orig = job_df
    alt = orig.copy()
    # Limit by time
    if end:
        from datetime import datetime, timedelta
        logger.info("Comparing start day {} with input {}".format(type(job_df['start_day']), datetime.strptime(start, "%Y-%m-%d").date() ))
        mask = (job_df['start_day'] > datetime.strptime(start, "%Y-%m-%d").date() - timedelta(days=1)) & (job_df['start_day'] <= datetime.strptime(end, "%Y-%m-%d").date())
        logger.debug("{} {}".format(start,end))
        job_df = job_df.loc[mask]
    # Here nclick tracks how many times new data is pressed
    # this is used to update if it has changed
    global nclick

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
    from math import ceil
    num_pages = ceil(len_jobs/int(rows_per_page))
    logger.debug("Pages = ceil({} / {}) = {}".format(len_jobs,int(rows_per_page),num_pages))
    logger.info("Update_output complete")
    return [
        alt.to_dict('records'),
        [{"name": i, "id": i} for i in alt.columns],
        'You\'ve entered: {}'.format(query),
        [dcc.Link(str(n+1)+", ",href="?page="+str(n)) for n in range((job_df.shape[0]//DEFAULT_ROWS_PER_PAGE))],
        int(rows_per_page),
        num_pages
    ]

######################## /Index Callbacks ######################## 

######################## Create Ref Callback ######################## 



######################## /Create Ref Callbacks ######################## 
