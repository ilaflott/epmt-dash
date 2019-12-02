from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime
import plotly.graph_objs as go
from plotly import tools
import numpy as np
import pandas as pd

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name
basicConfig(level=INFO)
pd.options.mode.chained_assignment = None


# Return dictionary query results
def parseurl(i):
    logger.info("Given URL {}".format(i))
    # convert url into dictionary
    from urllib.parse import parse_qs, urlparse
    return parse_qs(urlparse(i).query)





# Check if string time has 1 or 2 colons and convert grabbing just time
def conv_str_time(st):
    logger.info("Convert to time")
    import datetime
    if st.count(':') == 1:
        return datetime.datetime.strptime(st[1][1],"%H:%M").time()
    # limit functionality for now
    #if st.count(':') == 2:
    #    return datetime.datetime.strptime(st[1][1],"%H:%M:%S").time()
    else:
        return None

# Get greatest unit from df
power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P'}
def get_unit(alist):
    if len(alist) > 0:
        hi = max(alist)
    else:
        hi = 1
    from math import log
    #print(alist)
    return power_labels[int(log(hi,1024))]


# Convert df value used with get_unit
def convtounit(val,reqUnit):
    # Letter to Unit reverse search
    unitp = list(power_labels.keys())[list(power_labels.values()).index(reqUnit)]
    return val/1000**unitp
