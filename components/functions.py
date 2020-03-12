"""functions.py
Methods used for data manipulation from graphing to charting
"""

from urllib.parse import parse_qs, urlparse
from math import log
from colorsys import rgb_to_hsv, hsv_to_rgb
import time
from dash_config import MOCK_EPMT_API
from logging import getLogger
logger = getLogger(__name__)  
#pd.options.mode.chained_assignment = None

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


def gantt_me(jobs=[], gtags=None):
    """
    Generate Gantt chart data
    """
    start_times, end_times, op_name, op_dur, dfn = ([] for i in range(5))
    op = get_ops(jobs, tags = gtags, fmt='dict', full=True)

    # Roll ops into a zip
    for n in op:
        # Grossly extend a list for each metric to be graphed
        for k in n['intervals']:
            start_times.extend([k[0]])
            end_times.extend([k[1]])
            op_name.extend(["{}".format(list(n['tags'].items())[0])])
            op_dur.extend([n['duration']])
    rolled_ops = zip(op_name, start_times, end_times, op_dur)

    # Start times should be first
    rolled_ops = sorted(rolled_ops, key=lambda x: x[1])
    # Make gantt list of dicts from rolled_ops
    for g in rolled_ops:
        dfn.extend([{'Task':g[0],'Start':g[1],'Finish':g[2]}])
    return dfn


def create_gantt_graph(joblist=[],gtag=['op_instance','op']):
    """
    Generate the data to be graphed and supply it to the graphing
    function gantt_me.  Also do some minor formatting adjustments
    to the graph before returning the dash dcc graph object.
    """
    import plotly.figure_factory as ff
    import dash
    import dash_core_components as dcc
    
    gantt_data = gantt_me(jobs=joblist, gtags=gtag)
    gcolors = list_of_contrast(len(gantt_data),(33,45,237),0.05)
    fig = ff.create_gantt(gantt_data,colors=gcolors,bar_width=0.4,height=25*len(gantt_data)+150)
    fig.update_layout(title="Job {} Timeline for tag:'{}'".format(joblist,gtag),
    clickmode='event+select',)
    # Remove Year, week, day selector at top of gantt
    fig.layout.xaxis.rangeselector={}

    # op_sequence can be in the hundreds, turn off the y-axis labels
    if gtag is 'op_sequence':
        fig.update_yaxes(showticklabels=False)
    # Annotations disabled
    #fig = addAnnot(gantt_data,fig)
    basic_graph = dcc.Graph(
        id='basic-interactions',
        figure=fig
    )
    return basic_graph

def create_boxplot(jobs=['676007','625172','804285'], model="", normalize=True, metric='cpu_time', id=None):
    """boxplot wrapper"""
    import dash_core_components as dcc
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    #from epmt_query import get_ops, get_refmodels
    logger.debug("Creating boxplot")
    logger.debug("Jobs: {}".format(jobs))
    logger.debug("Normalize: {}".format(normalize))
    model_name = model
    logger.debug("Model: {}".format(model_name))
    jobs2test_against_model = jobs
    boxplot_title = metric + " Per Op: Jobs({}) ".format(', '.join(jobs2test_against_model))
    # Handle missing model
    try:
        jobs = get_refmodels(name=model_name)[0]['jobs']
        # Model exists include it in title
        boxplot_title = boxplot_title + " versus Model({})".format(model_name)
    except IndexError:
        jobs = []
        boxplot_title = boxplot_title + " {} model not found".format(model_name)


    # Include test jobs
    if jobs2test_against_model:
        jobs.extend(jobs2test_against_model)

    # Convert get_ops into list for all jobs
    op_list = []
    [op_list.extend(get_ops(jobby, tags = 'op', combine=False)) for jobby in jobs]
    ops_dur = pd.DataFrame([(op['jobs'][0].jobid, op['tags']['op'], op['proc_sums'][metric]) for op in op_list], columns=['jobid','op',metric])

    # Assign testjob column
    ops_dur['testjob'] = ops_dur['jobid'].apply(lambda n: True if n in jobs2test_against_model else False)
    
    x_title = metric

    # Check to apply normalization
    if normalize is 'True':
        boxplot_title = "Mean normalized " + boxplot_title
        # Mean Normalize
        ops_dur = df_normalizer(ops_dur, norm_metric=metric)
        x_title = x_title + "_normalized"
    
    # Create the model boxplot
    fig = px.box(ops_dur[(ops_dur['testjob']==False)], title=boxplot_title, x=x_title, y="op", hover_name="jobid", hover_data=[metric, x_title], orientation='h', points='suspectedoutliers')#, color='op')

    # Color outliers Red
    # only enabled if px.box(points='suspectedoutliers')
    # fig.update_traces(marker=dict(outliercolor='rgba(219, 64, 82, 0.6)'))


    # Filter dataframe for test jobs
    filtered = ops_dur[(ops_dur['testjob']==True)]

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
    fig.update_layout(showlegend=True,clickmode='event+select')

    basic_graph = dcc.Graph(
        id=id if id else 'basic-interactions',
        figure=fig
    )
    return basic_graph


def create_grouped_bargraph(title='',jobs=None, tags=None, y_value='component', metric=['duration','cpu_time'], order_by='duration', limit=10):
    import dash_core_components as dcc
    import plotly.express as px
    import pandas as pd
    jobs = get_jobs(tags=tags, limit=0, fmt='terse')
    logger.debug("Number of jobs to bargraph: {}".format(len(jobs)))
    if len(jobs) is 0:
        return "No Jobs Found"
    exp_jobs = get_jobs(jobs=jobs, fmt='dict', limit=limit)

    order_key_list = metric
    sum_dict = {}
    c_dict = {}
    for j in exp_jobs:
        if y_value is "component":
            c = j['tags']['exp_component']
        elif y_value is 'jobid':
            c = j['jobid']
        entry = c_dict.get(c, {'data': []})
        entry['data'].append((j['tags']['exp_time'], j['jobid'], [j[ok] for ok in order_key_list]))
        c_dict[c] = entry

    comps = []

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
    import operator
    sorted_d = sorted(sum_dict.items(), key=lambda x: x[1][order_by])

    # Select up to including the limit
    if limit is 0:
        logger.debug("Limit set to 0, Defaulting limit to 10")
        limit = 10
    sorted_d = sorted_d[:limit]
    import plotly.graph_objects as go

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
    fig.update_layout(xaxis_type="log",
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
