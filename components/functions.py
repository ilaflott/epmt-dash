"""functions.py
Methods used for data manipulation
"""

from logging import getLogger
from urllib.parse import parse_qs, urlparse
from math import log
from colorsys import rgb_to_hsv, hsv_to_rgb
import time
from epmt_query import get_procs
# We log how we want
# pylint: disable=invalid-name, logging-format-interpolation
logger = getLogger(__name__)  # you can use other name
#pd.options.mode.chained_assignment = None


# Return dictionary query results
def parseurl(i):
    """ parseurl
    Accepts url & returns query parameter
    """
    logger.info("Given URL {}".format(i))
    # convert url into dictionary
    res_dict = parse_qs(urlparse(i).query)
    if ',' in res_dict['jobid'][0]:
        res_dict['jobid'] = res_dict['jobid'][0].split(',')
    logger.info("URL2Dict {}".format(res_dict))
    return res_dict



def recent_button(btn_dict):
    """ recent_button
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
    #print(alist)
    return power_labels[int(log(hi, 1024))]


def convtounit(val, reqUnit):
    """
    Helper function accepts a value & a unit
    Input: bytes, power_label unit
    Output: Value converted
    """
    # Letter to Unit reverse search
    unitp = list(power_labels.keys())[list(power_labels.values()).index(reqUnit)]
    return val/1000**unitp


def contrasting_color(color):
    """contrasting_color
    This helper function returns a shifted hsv color.
    Input: color list [h,s,v]
    Output: (r,g,b), hex of color
    """
    if not color:
        return None

    # How much to jump in hue:
    jump = .16
    (r, g, b) = hsv_to_rgb(color[0] + jump,
                           color[1],
                           color[2])
    hexout = '#%02x%02x%02x' % (int(r), int(g), int(b))
    return ((r, g, b), hexout)
((r, g, b), hex) = contrasting_color(rgb_to_hsv(50, 100, 200))


def list_of_contrast(length, start=(0, 0, 0)):
    """ list_of_contrast
    Returns a list of colors of requested length with requested starting r,g,b value
    """
    l = []
    for _ in range(length):
        ((r, g, b), hex) = contrasting_color(rgb_to_hsv(start[0], start[1], start[2]))
        l.append(hex)
        start = (r, g, b)
    return l

def durList(jid, minDur, maxDur, exes):
    """Takes jobid, and limiting paramaters for query"""
    print("Building data Dict for", jid)
    print("Querying DB...")
    start = time.time()
    # TODO
    logger.info("Limiting procs to 15k")
    procList = get_procs(jid, limit=15000) #, fltr=lambda p: p.duration > minDur and maxDur > p.duration, order='desc(p.exclusive_cpu_time)', fmt='dict')
    end = time.time()
    print("Took",(end - start))
    #print("Sorting and Filtering ",len(procList))
    #procList = procList[0::density]
    #print("After ", len(procList))
    # print("loop:",tuple(i for i in options))
    # x value is start time, y variable index on options
    exenames = list(set([k['exename'] for k in procList]))
    opnames = [list(k['tags'].keys() if k['tags'] is not None else "") for k in procList][0]
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
    """Break query results into separate traces"""
    from collections import defaultdict
    outputDict = defaultdict(list)
    #print("graphstyle", graphStyle)
    for entry in data:
        if (graphStyle[:4] == "tag-"):
            # Works but dirty
            # outputDict[sum(entry[graphStyle].items(),())].append([entry])
            outputDict[entry['tags'][graphStyle[4:]]].append([entry])
        else:
            outputDict[entry[graphStyle]].append([entry])
        #print([sublist[0]['start'] for sublist in outputDict['dash']])
    hoverwidth = 20
    output = [{  # 'x': list(range(1, 11)), 'y': list(range(1, 11)),
              'mode': 'markers',
              'x': [sublist[0]['start'] for sublist in outputDict[n]],
              'y': [sublist[0]['duration'] for sublist in outputDict[n]],
              'text' if (True) else None: [[sublist[0]["exename"],sublist[0]["args"],sublist[0]["path"]] for sublist in outputDict[n]],
              'hoverinfo':"text",
              'name': n,
              'hovertemplate': "Path: %{text[2]}<br>" +
                                "Args: <br>%{text[1]}"
              #'textposition': 'top center'
              } for n in outputDict.keys()]
    #print(output)
    #
    #textwrap.wrap("Path: %{text[2]}<br>" + "Args: <br>%{text[1]}", hoverwidth)
    # print("args: {0}".format("<br>".join(textwrap.wrap(longstring,hoverwidth))))
    return output