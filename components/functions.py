"""functions.py
Methods used for data manipulation from graphing to charting
"""

from urllib.parse import parse_qs, urlparse
from math import log
from colorsys import rgb_to_hsv, hsv_to_rgb
import pandas as pd
import time
from dash_config import MOCK_EPMT_API
from logging import getLogger
logger = getLogger(__name__)  
#pd.options.mode.chained_assignment = None

class InterfaceError(Exception):
    pass

if MOCK_EPMT_API:
    logger.info("Using Mock API")
    from epmt_query_mock import get_procs, get_ops, get_refmodels, get_jobs
else:
    logger.info("Using EPMT API")
    from epmt_query import get_procs, get_ops, get_refmodels, get_jobs

# Return dictionary query results
def parseurl(i):
    """ 
    This Function uses urllib to parse a query then
    checks each of the query keys values for commas and converts
    those values into lists.
    Accepts url & returns query dictionary.
    """
    logger.info("Given URL {}".format(i))

    # Determine graphstyle and jobid

    # convert url into dictionary
    res_dict = parse_qs(urlparse(i).query)
    logger.debug("URL parse_qs: {}".format(res_dict))
    # Parse query key values, values for commas
    # TODO: A better method may be encoding or repeating the key
    # https://stackoverflow.com/a/50537278
    for field in res_dict.keys():
        if ',' in res_dict[field][0]:
            res_dict[field] = res_dict[field][0].split(',')
    logger.info("URL2Dict {}".format(res_dict))
    return res_dict


def recent_button(btn_dict):
    """ 
    This function accepts a dictionary of buttons, tabs and timestamps
     and returns the most recent one clicked.
    Input: dictionary of buttons timestamps
    If Model tab was clicked:
     {'button1':0, 'button2':0, 'button3':0, 'tabs':'model'}
    If Button2 was clicked recently:
      {'button1':352512, 'button2':952512, 'button3':152512, 'tabs':None}
    Returns: Recent button clicked or None
    """
    # If Tab was clicked return none
    if btn_dict.get('tabs'):
        logger.debug("Tab {} Was clicked".format(btn_dict['tabs']))
        return None
    else:
        # Tab was not clicked remove it from dictionary for latter max calculation
        btn_dict.pop('tabs', None)
    if sum(btn_dict.values()) > 0:
        recent = max(btn_dict, key=lambda key: btn_dict[key])
        logger.debug("Button click {}".format(recent))
        return recent
    return None


power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P'}


def get_unit(alist):
    """

    Get greatest unit from df alist

    """
    if len(alist) > 0:
        hi = max(alist)
    else:
        hi = 1
    # print(alist)
    return power_labels[int(log(hi, 1024))]


def convtounit(val, reqUnit):
    """

    This function converts a given byte to requested unit.
    Helper function accepts a value & a unit
    Input: bytes, power_label unit
    Output: Value converted without label.

    """
    # Letter to Unit reverse search
    unitp = list(power_labels.keys())[list(power_labels.values()).index(reqUnit)]
    return val/1000**unitp


def contrasting_color(color,shift=0.16):
    """

    This helper function returns a shifted hsv color 
    and matching hex value for convience.

    Input: color list [h,s,v]
    Output: (r,g,b), hex of color

    Example:
    ((r, g, b), hex) = contrasting_color(rgb_to_hsv(50, 100, 200))

    """
    if not color:
        return None

    (r, g, b) = hsv_to_rgb(color[0] + shift,
                           color[1],
                           color[2])
    hexout = '#%02x%02x%02x' % (int(r), int(g), int(b))
    return ((r, g, b), hexout)


def list_of_contrast(length, start=(33, 45, 237), hue_shift=0.16):
    """
    Returns a list of colors of requested length
    with requested starting r,g,b tuple.

    length: Number of hex values to return
    start = rgb tuple
    hue_shift = hue adjustment factor added to the hsv

    """
    l = []
    for _ in range(length):
        ((r, g, b), hex) = contrasting_color(rgb_to_hsv(start[0], start[1], start[2]),hue_shift)
        l.append(hex)
        start = (r, g, b)
    return l


def durList(jid, minDur, maxDur, exes):
    """

    This Function will convert jobid's into traces for graphing.
    Takes jobid, and limiting paramaters for query

    minDur & maxDur will reduce the procs returned to only
    those requested.

    exes will be a list of those exename procs that are requested

    """
    logger.debug("Building data Dict for {}".format(jid))
    logger.debug("Querying DB...")
    start = time.time()
    # TODO
    proc_limit = None
    logger.warning("Limiting procs to {}".format(proc_limit))
    # , fltr=lambda p: p.duration > minDur and maxDur > p.duration, order='desc(p.exclusive_cpu_time)', fmt='dict')
    procList = get_procs(jid, limit=proc_limit)
    end = time.time()
    print("Took", (end - start))
    #print("Sorting and Filtering ",len(procList))
    #procList = procList[0::density]
    #print("After ", len(procList))
    # print("loop:",tuple(i for i in options))
    # x value is start time, y variable index on options
    exenames = list(set([k['exename'] for k in procList]))
    opnames = set(k['tags'].get('op', 'no-tag') for k in procList)
    traceList = [{'label': 'Executable Name', 'value': 'exename'},
                 {'label': 'Job', 'value': 'job'},
                 {'label': 'Host', 'value': 'host'},
                 {'label': 'Exit Code', 'value': 'exitcode'}]
    for n in opnames:
        traceList.append({'label': n.capitalize(), 'value': "tag-" + n})
    exenames.sort(key=str.lower)
    if(exes):  # Leaves alot of empty dicts, dropdown seems to ignore them
        filteredData = []
        for x in procList:
            if x['exename'] in exes:
                filteredData.append(x)
        # old xyData = [{key:val for key, val in e.items() if val[1] in exes} for e in procList]
        procList = filteredData
    return procList, exenames, traceList


def separateDataBy(data, graphStyle="exename", pointText=("path", "exe", "args"), ):
    """
    This function takes traceLists as data and transposes them 
    by the requested graphstyle.
    Graphstyle options are tag-ops, exename or other tag paramaters
    (tag-instance or tag-sequence)

    """
    from collections import defaultdict
    outputDict = defaultdict(list)
    #print("graphstyle", graphStyle)
    for entry in data:
        if (graphStyle[:4] == "tag-"):
            # Works but dirty
            # outputDict[sum(entry[graphStyle].items(),())].append([entry])
            if entry['tags'].get('op', None):
                outputDict[entry['tags'][graphStyle[4:]]].append([entry])
        else:
            outputDict[entry[graphStyle]].append([entry])
        #print([sublist[0]['start'] for sublist in outputDict['dash']])
    hoverwidth = 20
    output = [{  # 'x': list(range(1, 11)), 'y': list(range(1, 11)),
              'mode': 'markers',
              'x': [sublist[0]['start'] for sublist in outputDict[n]],
              'y': [sublist[0]['duration'] for sublist in outputDict[n]],
              'text' if (True) else None: [[sublist[0]["exename"], sublist[0]["args"], sublist[0]["path"]] for sublist in outputDict[n]],
              # 'hoverinfo':"text",
              'hovermode':False,
              'name': n,
              # 'hovertemplate': "Path: %{text[2]}<br>" +
              #                  "Args: <br>%{text[1]}"
              # 'textposition': 'top center'
              } for n in outputDict.keys()]
    # print(output)
    #
    #textwrap.wrap("Path: %{text[2]}<br>" + "Args: <br>%{text[1]}", hoverwidth)
    # print("args: {0}".format("<br>".join(textwrap.wrap(longstring,hoverwidth))))
    return output


def df_normalizer(df, idx='op', norm_metric='cpu_time'):
    """
    Simple mean normalizer algorithm that works on dataframes.
    Will create a new column titled the value from norm_metric
    Normalized Column: (norm_metric)_normalized
    """
    df = df.set_index(idx)
    means_stds = df.groupby(idx)[norm_metric].agg(['mean','std']).reset_index()
    df = df.merge(means_stds,on=idx)
    df[norm_metric +'_normalized'] = (df[norm_metric] - df['mean']) / df['std']
    return df

# Incomplete, could be extended to apply text to each bar on gantt chart
# x_pos/y_pos need work
# def addAnnot(df, fig):
#     for i in df:
#         x_pos = (i['Finish'] - i['Start'])/2 + i['Start']
#         for j in fig['data']:
#             y_pos = (j['y'][0] + j['y'][1] + j['y'][2] + j['y'][3])/4
#         fig['layout']['annotations'] += tuple([dict(x=x_pos,y=y_pos,text=i['Task'],font={'color':'black'})])
#     return fig


def gantt_me(jobs=[], gtags=None, exp_name=None, exp_component=None):
    """
    Generate Gantt chart data
    """
    start_times, end_times, op_name, op_dur, dfn = ([] for i in range(5))
    if jobs:
        logger.debug("Job was passed, get ops: {}".format(jobs))
        a = get_ops(jobs, tags=gtags, fmt='pandas', full=True)
        # Bump Op out
        a['op'] = a['tags'].apply(lambda x: x.get('op'))

        # Setup dataframe for gantt data
        gantt_data_df = pd.DataFrame(columns=['Start','Finish','Task'])

        # iterate each op row
        for index, op in a.iterrows():
            # Take 'intervals' tuple and iterate it
            intervs = op['intervals']
            for n in intervs:
                # Store each interval as a op start and finish time
                gantt_data_df = gantt_data_df.append({'Start':n[0],'Finish':n[1],'Task':op['op'], 'Resource':op['op']}, ignore_index=True)
        # Order gantt data by start time
        gantt_data_df = gantt_data_df.sort_values('Start')

        gantt_title = ','.join(jobs) + " timeline by operation " + ','.join(gtags)
    elif exp_name:
        logger.debug("experiment was passed: {}".format(exp_name))
        if exp_component:
            logger.debug("Component was passed: {}".format(exp_component))
            gantt_data_df = get_jobs(tags={'exp_name':exp_name, 'exp_component':exp_component}, fmt='pandas')
            gantt_data_df = gantt_data_df[['start','end','jobid']]
            gantt_data_df['Resource'] = gantt_data_df['jobid']
            gantt_data_df = gantt_data_df.rename(columns={'start': 'Start', 'end': 'Finish', 'jobid':'Task' })
            gantt_title = exp_name + " timeline for component " + exp_component
        else:
            # Return just jobs we only have a exp_name.
            # todo: handle catchall case
            gantt_data_df = get_jobs(tags={'exp_name':exp_name}, fmt='pandas', limit=0)
            # Extract component
            gantt_data_df['exp_component'] = gantt_data_df['tags'].apply(lambda x: x.get('exp_component'))
            gantt_data_df = gantt_data_df[['start','end','exp_component','jobid']]
            gantt_data_df = gantt_data_df.rename(columns={'start': 'Start', 'end': 'Finish', 'exp_component':'Resource', 'jobid':'Task' })
            gantt_title = exp_name + " timeline by component "
    else:
        return None
    gantt_data_df = gantt_data_df.dropna()
    gcolors = list_of_contrast(len(gantt_data_df),(33,45,237),0.06)
    return (gantt_data_df, gantt_title, gcolors)



def create_gantt_graph(joblist=[],gtag=['op'],exp_name=None, exp_component=None):
    """
    Generate the data to be graphed and supply it to the graphing
    function gantt_me.  Also do some minor formatting adjustments
    to the graph before returning the dash dcc graph object.
    """
    import plotly.figure_factory as ff
    import dash
    import dash_core_components as dcc
    
    (gantt_data, gantt_title, gantt_colors) = gantt_me(jobs=joblist, gtags=gtag, exp_name=exp_name, exp_component=exp_component)
    if gantt_data is None:
        return "Could not get operations or jobs"
    logger.debug("Len of gantt data {} first 2 \n{}".format(len(gantt_data), gantt_data.head(2)[['Start','Task','Resource']]))
    fig = ff.create_gantt(gantt_data,group_tasks=True, index_col='Resource', show_colorbar=True, colors=gantt_colors,bar_width=0.4,height=600) #5*len(gantt_data)+150)
    fig.update_layout(title=gantt_title, clickmode='event+select',)
    # Remove Year, week, day selector at top of gantt
    fig.layout.xaxis.rangeselector={}
    fig.layout.legend.traceorder = "normal"
    logger.debug("Trace layout legend: {}".format(fig.layout.legend))
    # op_sequence can be in the hundreds, turn off the y-axis labels
    if gtag is 'op_sequence':
        fig.update_yaxes(showticklabels=False)
    # Annotations disabled
    #fig = addAnnot(gantt_data,fig)
    basic_graph = dcc.Graph(
        # Return basic-interactions-end if we're on final gantt
        # To stop any new callbacks from firing
        id='basic-interactions-end' if joblist else 'basic-interactions',
        figure=fig
    )
    return basic_graph

def create_boxplot(jobs=[], model="", normalize=True, metric='cpu_time', tags='op', box_title='', id=None):
    """
    Create a boxplot based on a model with sample jobs scattered over it, 
    tags currently only work for: 
        general strings: 'op' or 'op_instance'
        single dictionaries: {'op':'hsmget', 'op_instance':2}

    jobs(optional): A list of jobids to scatter over the boxplot
    model(optional): A model name to act as the boxplot
    normalize: Will normalize jobs and model jobs as long as there are at least
                3 in total.
    metric: A single metric from op proc_sums to graph against
    tags: tag string or dictionary to search on, default: 'op'
    box_title(optional): A supplied title otherwise one will be generated
    id: Dash graph object id name for callback reference
    """
    import dash_core_components as dcc
    import plotly.graph_objects as go
    import plotly.express as px
    from json import dumps
    #from epmt_query import get_ops, get_refmodels
    logger.debug("Creating boxplot")
    logger.debug("Jobs: {}".format(jobs))
    logger.debug("Normalize: {}".format(normalize))
    model_name = model
    # Passed in jobs to scatter over model box
    sample_jobs = []
    fig = go.Figure()
    ops_dur = pd.DataFrame()
    model_jobs = []
    gen_box_title = metric + " Per " + dumps(tags) + " "

    if jobs:
        sample_jobs = jobs
        gen_box_title = gen_box_title + "Jobs({})".format(', '.join(sample_jobs))

    if model_name:
        try:
            model_jobs = get_refmodels(name=model_name)[0]['jobs']
            # Model exists include it in title
            if jobs:
                gen_box_title = gen_box_title + ' versus '
            gen_box_title = gen_box_title + "Model: {}".format(model_name)
            logger.debug("Model: {} has jobs: {}".format(model_name, model_jobs))
        except IndexError:
            model_jobs = []
            return "Could not find given " + model_name

        # Include model jobs
        for job in model_jobs:
            logger.info("Calculating {} for model job {}".format(tags, job))
            df = get_ops(job, tags=tags, combine=False,fmt='pandas')
            df['Type'] = 'Model'
            ops_dur = ops_dur.append(df, sort=False)
    
    # Include sample jobs
    for job in sample_jobs:
        logger.info("Calculating {} for sample job {}".format(tags, job))
        df = get_ops(job, tags=tags, combine=False,fmt='pandas')
        df['Type'] = 'Sample'
        ops_dur = ops_dur.append(df, sort=False)
    ops_dur[metric] = ops_dur['proc_sums'].apply(lambda x: x.get(metric))
    ops_dur['op'] = ops_dur['tags'].apply(dumps)
    ops_dur['jobid'] = ops_dur['jobs'].apply(lambda x: x[0])

    x_title = metric

    # Check to apply normalization
    # Models must have a minimum number of jobs
    # Sample can be run without model, don't normalize a few samples
    if normalize is 'True' and (len(sample_jobs) + len(model_jobs)) > 3:
        gen_box_title = "Mean normalized " + gen_box_title
        # Mean Normalize
        ops_dur = df_normalizer(ops_dur, norm_metric=metric)
        x_title = x_title + "_normalized"
    
    # Create the model boxplot on model_jobs
    if model_jobs:
        fig = px.box(ops_dur[(ops_dur['Type']=='Model')], x=x_title, y="op", hover_name="jobid", hover_data=[metric, x_title], orientation='h', points='all')#, color='op')

    # Color outliers Red
    # only enabled if px.box(points='suspectedoutliers')
    # fig.update_traces(marker=dict(outliercolor='rgba(219, 64, 82, 0.6)'))


    # Filter dataframe for test jobs
    filtered = ops_dur[(ops_dur['Type'] =='Sample')]

    # Get unique jobids from filtered list
    uniq_job_ops = filtered.jobid.unique()

    # Dataframe to graph
    df_to_scatter = [filtered[(filtered['jobid']==job)] for job in uniq_job_ops]

    # Scatter the test jobs against the model
    [fig.add_trace(
        go.Scatter(
            mode='markers',
            x=job[x_title],
            y=job['op'],
            opacity=1,
            name=job.head(1).jobid.to_string(index=False),
            text=job.jobid,
            hoverinfo='text',
            marker=dict(
                #color='LightSkyBlue',
                size=10,
                line=dict(
                    #color='Green',
                    width=2
                )
            ),
            showlegend=True
        )
) for job in df_to_scatter]

    # Display legend for scatter points
    fig.update_layout(showlegend=True, clickmode='event+select',
                      title=box_title if box_title else gen_box_title)

    basic_graph = dcc.Graph(
        id=id if id else 'model-boxplot',
        figure=fig
    )
    return basic_graph


def create_grouped_bargraph(title='',jobs=None, tags=None, y_value='component', metric=['duration','cpu_time'], ops='op', order_by='duration', limit=10):
    """
    
    Horizontal bargraph because the Y axis names are easier to read
    and there can be alot of bars to plot.
    """
    import dash_core_components as dcc
    import plotly.graph_objects as go
    import plotly.express as px
    import operator
    
    # Convert list query of jobs into single jobid
    # if only a single job exists
    if jobs and len(jobs) == 1:
        jobs = jobs[0]
    if y_value is 'op':
        logger.debug("Get ops of jobs: {}".format(jobs))
        job_ops = get_ops(jobs=jobs, tags=ops)
    else:
        # Get jobs in dict format.
        # todo: this should be pandas
        exp_jobs = get_jobs(jobs=jobs, tags=tags, fmt='dict')
        if len(exp_jobs) is 0:
            return "No Jobs Found"
        logger.debug("Number of jobs to bargraph: {}".format(len(exp_jobs)))

    order_key_list = metric
    sum_dict = {}
    
    # Component dictionary contains key of data value of 
    # component: data: (exp_time, jobid, [metrics,])
    #
    # example 1 component, 1 jobid with 2 metrics: 
    # {'aerosol_cmip': {'data': [('18540101',
    #                             '2444929',
    #                             [18941050858.0, 4863690779.0]),
    # todo:
    # This can be more easily achieved with pandas.
    c_dict = {}
    #try:
    if y_value is 'op':
        for o in job_ops:
            if y_value is "op":
                c = o['tags'][ops]
            entry = c_dict.get(c, {'data': []})
            entry['data'].append(("", o['jobs'][0].jobid, [o['proc_sums'][ok] for ok in metric]))
            c_dict[c] = entry
    else:
        for j in exp_jobs:
            if y_value is "component":
                c = j['tags']['exp_component']
            elif y_value is 'jobid':
                c = j['jobid']
            entry = c_dict.get(c, {'data': []})
            entry['data'].append((j['tags']['exp_time'], j['jobid'], [j[ok] for ok in order_key_list]))
            c_dict[c] = entry
#    except KeyError as ke:
        #return "Key Missing"

    comps = []

    # This loop generates the sum_dict
    # sum_dict contains key of component
    # value of dictionary of metrics
    # Key metric : value metric sum generated from the c_dict
    for ok in order_key_list:
        for c,v in c_dict.items():
            comps.extend([c])
            # Reset collection list for each okl
            lis = []
            for g in v['data']:
                lis.extend([g[2][order_key_list.index(ok)]])
                # assign list to collection dict
                if c in sum_dict:
                    sum_dict[c].update({ok:lis})
                else:
                    sum_dict[c] = {ok:lis}
            sum_dict[c][ok] = sum(sum_dict[c][ok])

    # Generate sorted list on order_by key
    # This only sorts and limits 
    if order_by not in metric:
        logger.info("{} is not in metrics, ordering by {}".format(order_by,metric[0]))
        order_by = metric[0]
    sorted_d = sorted(sum_dict.items(), key=lambda x: x[1][order_by])

    if limit > 0:
        sorted_d = sorted_d[-limit:]
    fig = go.Figure()
    color = {}
    color['cpu_time'] = 'rgb(180, 160, 109)'
    color['duration'] = 'rgb(26, 118, 255)'
    color['num_procs'] = 'rgb(75, 83, 50)'
    color['num_threads'] = 'rgb(140, 83, 109)'
    for m in order_key_list:
        fig.add_trace(go.Bar(y=[n[0] for n in sorted_d], #component c
                        x=[l[1][m] for l in sorted_d], # List of m values in component c
                        name=m,
                        marker_color=color[m],
                        orientation='h'
                        ))

    # Logarithmic metric, descending
    fig.update_layout(#xaxis_type="log",
                      # xaxis={'categoryorder':'category descending'}),
                      xaxis_tickfont_size=17,
                      xaxis=dict(
                          titlefont_size=20
                      ),
                      barmode='group',
                      bargap=0.20,
                      # Graph height is function of jobs and metrics
                      # Add minimum 200px for small graphs
                      height=25*len(metric)*len(sorted_d) + 200,
                      clickmode='event+select',
                      title=title
                      #title=exp_name + " top " + str(limit) + " " + ", ".join(order_key_list) + " per component"
                      )
    if y_value is 'jobid':
        fig.update_layout(yaxis=dict(type='category'))
    basic_graph = dcc.Graph(
        id='bargraph',
        figure=fig
    )
    return basic_graph


def create_stacked_bar(jobs=None,metrics=None, normalize=True,order='total'):
    import plotly.graph_objects as go

    # Convert jobs and metrics into traces
    data = trace_renderer(jobs,metrics,normalize)

    layout = go.Layout(
        barmode='stack',
        # Across the bottom is each job
        xaxis=dict(tickvals=jobs, type='category')
    )
    if order is not 'total' and order is not None:
        logger.debug("Ordering by: {}".format(order))
        jobs=get_jobs(jobs=jobs,fmt='dict',limit=0)
        sort_data = [(j['jobid'],j[order]) for j in jobs]
        sort_data.sort(key=lambda tup: tup[1], reverse=False)
        sorted_jobids = [j[0] for j in sort_data]
        layout.xaxis.update(dict(categoryorder='array', categoryarray=sorted_jobids))
        layout.title = ', '.join(metrics)+ " ordered by " + order
    else:
        layout.xaxis.update(dict(categoryorder='total descending'))
        layout.title = ', '.join(metrics)+ " ordered by category total"
    
    fig = go.Figure(data=data, layout=layout)
    return fig

def trace_renderer(jobs=None,metrics=None, normalize=True):
    """
    Returns list of traces
    """
    import plotly.graph_objects as go
    # For stacked bar the x values are embedded in each trace
    # Only trace Data list is returned
    data = []

    # Traces go vertical, Jobs go horizontal
    job_dicts = get_jobs(jobs,fmt='dict',limit=0)
    for m in metrics:
        data.append(go.Bar(
        x=jobs, y=[j[m] for j in job_dicts],
        name=m
    ))
    if normalize:
        from epmt_stat import normalize
        for d in data:
            d['y'] = normalize(d['y'],min_=-1/len(metrics), max_=1/len(metrics))
    return data


def data_gatherer_ops(jobs=None, metric=['duration'], tag_value='op'):

    a = get_ops(jobs[0], tags=tag_value, fmt='pandas', full=True)
    if len(jobs)>1:
        for j in jobs[1:]:
            a = a.append(get_ops(j, tags=tag_value, fmt='pandas', full=True))
    
    # Bump jobid out as string
    a['jobid'] = a['jobs'].apply(lambda x: x[0])

    if isinstance(tag_value,dict):
        a[str(tag_value)] = str(tag_value)
    else:
        # Bump Op out
        a[tag_value] = a['tags'].apply(lambda x: x.get(tag_value))

    
    # bump requested metrics out
    for m in metric:
        a[m] = a['proc_sums'].apply(lambda x: x.get(m))

    return a

def bar_graph(graph_df=None, jobs=None, x=None, y=None, exp_name=None, group_on=None, tag_value=None, as_group=True, horizontal=True, title=None):
    '''
    as_group: True groups data, False stacks data
    '''
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.figure_factory as ff
    
    # No dataframe to graph was given, we will build one
    # Currently only works for ops
    # Requires jobs & tag_value
    if graph_df.empty:
        logger.debug("No dataframe passed, calculating now...")
        graph_df = data_gatherer_ops(jobs=jobs, metric=x, tag_value=tag_value)
        # if component data  :: data_gatherer_component()
        # if proc data
        # if thread data  :: get_thread_metrics

    fig = go.Figure()
    # if x or y are a list we should iterate the list and use go.Bar
    # rather than px.bar
    if isinstance(x,list):
        for k in x:
            fig = go.Figure(data=[go.Bar(name=a, x=graph_df[a], y=graph_df[y], orientation='h' if horizontal else 'v') for a in x])
    elif isinstance(y,list):
        for k in y:
            fig = go.Figure(data=[go.Bar(name=b, x=graph_df[b], y=graph_df[y], orientation='h' if horizontal else 'v') for b in y])
    else:
        fig = px.bar(graph_df, x=x, y=y, orientation='h' if horizontal else 'v', color=None if not group_on else group_on) #group_on

    
    # jobid's are better displayed as category
    # not interpreted as integers
    if y == 'jobid':
        fig.update_layout(yaxis_type='category')
    if x == 'jobid':
        fig.update_layout(xaxis_type='category')

    if as_group:
        fig.update_layout(barmode='group')
    fig.update_layout(width=800,clickmode='event+select')
    
    # Generate a title based on given data
    if not title:
        gen_title = ''
        if exp_name:
            gen_title = gen_title + "exp_name: " + exp_name
        if tag_value:
            gen_title = gen_title + " & tag value:" + str(tag_value)
        gen_title = 'Y: ' + ','.join(y) if isinstance(y,list) else y 
        gen_title = gen_title + " X:" + ','.join(x) if isinstance(x,list) else x
    fig.update_layout(title= gen_title if not title else title,
    xaxis_title=', '.join(x) if isinstance(x,list) else x,
    yaxis_title=', '.join(y) if isinstance(y,list) else y)
    
    return fig


def graph_components(exp_name=None, exp_component=None, jobs=None, title=None, metric=None, order=None):
    """
    This Function accepts components to graph Jobid's on the Y axis
    """
    logger.info("Graph Components")
    # build component dataframe
    df = get_jobs(jobs=jobs, tags={'exp_name':exp_name, 'exp_component':exp_component}, fmt='pandas')
    # render graph
    logger.debug("Order received: {}".format(order))
    df = df.sort_values([order if order is not None else metric[0]])
    graph = bar_graph(graph_df=df, y='jobid', x=metric, title=title)
    return graph


def graph_jobs(exp_name=None, jobs=None, metric=['duration'], title=None):
    """
    This Function accepts experiments to graph components
    """
    logger.info("Graph Jobs")
    # build jobs dataframe
    df = get_jobs(jobs=jobs, tags={'exp_name':exp_name}, fmt='pandas')
    df['component'] = df['tags'].apply(lambda x: x.get('exp_component'))
    grouped_df = df.groupby('component', as_index=False).agg({e:'sum' for e in metric})
    # render graph
    grouped_df = grouped_df.sort_values([metric[0]])
    graph = bar_graph(graph_df=grouped_df, y='component', x=metric, horizontal=True, title=title)
    return graph


def graph_ops(jobs=None, tag_value=None, metric=['duration'], title=None):
    """
    This Function accepts Jobs to graph Operations
    """
    logger.info("Graph Ops")
    # build ops dataframe
    df = data_gatherer_ops(jobs=jobs, tag_value=tag_value, metric=metric)
    # render graph
    df = df.sort_values([metric[0]])
    graph = bar_graph(graph_df=df, y=tag_value, x=metric, group_on=metric, title=title)
    return graph
