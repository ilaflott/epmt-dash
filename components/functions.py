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
    from epmt_query_mock import get_procs
else:
    logger.info("Using EPMT API")
    from epmt_query import get_procs, get_ops


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


def gantt_me(jobs=[], gtags=['op']):
    """Generate Gantt chart data"""
    start_times, end_times, op_name, op_dur, dfn = ([] for i in range(5))
    e = get_procs()[:1]
    logger.error(e)
    op = get_ops(jobs, tags = gtags, fmt='orm')

    # Roll ops into a zip
    for n in op:
        # Grossly extend a list for each metric to be graphed
        start_times.extend([n.start])
        end_times.extend([n.finish])
        op_name.extend(["{}".format(list(n['tags'].items())[0])])
        op_dur.extend([n.duration])
    rolled_ops = zip(op_name, start_times, end_times, op_dur)

    # Start times should be first
    rolled_ops = sorted(rolled_ops, key=lambda x: x[1])
    # Make gantt list of dicts from rolled_ops
    for g in rolled_ops:
        dfn.extend([{'Task':g[0],'Start':g[1],'Finish':g[2]}])
    return dfn


def create_gantt_graph():
    """gantt_me wrapper"""
    import plotly.figure_factory as ff
    import dash
    import dash_core_components as dcc
    joblist = ['625172']
    gtag = ['op_instance','op']
    gantt_data = gantt_me(joblist, gtag)
    gcolors = list_of_contrast(len(gantt_data),(33,45,237),0.05)
    fig = ff.create_gantt(gantt_data,colors=gcolors,bar_width=0.4)
    fig.update_layout(title="Job {} Timeline for tag:'{}'".format(joblist,gtag))
    # Remove Year, week, day selector at top of gantt
    fig.layout.xaxis.rangeselector={}

    # op_sequence can be in the hundreds, turn off the y-axis labels
    if gtag is 'op_sequence':
        fig.update_yaxes(showticklabels=False)
    basic_graph = dcc.Graph(
        id='basic-interactions',
        figure=fig
    )
    return basic_graph

def create_boxplot():
    """boxplot wrapper"""
    import plotly.figure_factory as ff
    import dash
    import dash_core_components as dcc
    basic_graph = dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': [1, 2, 3, 4],
                    'y': [4, 1, 3, 5],
                    'text': ['a', 'b', 'c', 'd'],
                    'customdata': ['c.a', 'c.b', 'c.c', 'c.d'],
                    'name': 'Trace 1',
                    'mode': 'markers',
                    'marker': {'size': 12}
                },
                {
                    'x': [1, 2, 3, 4],
                    'y': [9, 4, 1, 4],
                    'text': ['w', 'x', 'y', 'z'],
                    'customdata': ['c.w', 'c.x', 'c.y', 'c.z'],
                    'name': 'Trace 2',
                    'mode': 'markers',
                    'marker': {'size': 12}
                }
            ],
            'layout': {
                'title': 'Boxplot Placeholder',
                'clickmode': 'event+select'
            }
        }
    )
    return basic_graph
