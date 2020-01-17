from datetime import datetime as dt
from datetime import datetime, timedelta
from logging import getLogger

#import pandas as pd

logger = getLogger(__name__)  # you can use other name
#pd.options.mode.chained_assignment = None


# Return dictionary query results
def parseurl(i):
    """ parseurl
    Accepts url & returns query parameter
    """
    logger.info("Given URL {}".format(i))
    # convert url into dictionary
    from urllib.parse import parse_qs, urlparse
    res_dict = parse_qs(urlparse(i).query)
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
    # Get greatest unit from df
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

import colorsys
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
    (r,g,b) = colorsys.hsv_to_rgb(color[0] + jump,
                                  color[1],
                                  color[2])
    hexout = '#%02x%02x%02x' % (int(r),int(g),int(b))
    return ((r,g,b),hexout)
((r,g,b), hex)= contrasting_color(colorsys.rgb_to_hsv(50, 100, 200))


def list_of_contrast(length, start=(0,0,0)):
    """ list_of_contrast
    Returns a list of colors of requested length with requested starting r,g,b value
    """
    l = []
    for n in range(length):
        ((r,g,b),hex) = contrasting_color(colorsys.rgb_to_hsv(start[0],start[1],start[2]))
        l.append(hex)
        start = (r, g, b)
    return l
