from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime
import plotly.graph_objs as go
from plotly import tools
import numpy as np
import pandas as pd

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

pd.options.mode.chained_assignment = None


# Return dictionary query results
def parseurl(i):
    logger.info("Given URL {}".format(i))
    # convert url into dictionary
    from urllib.parse import parse_qs, urlparse
    return parse_qs(urlparse(i).query)


# Grabs sample reference models, formats them and returns them.
def get_references():
    import refs
    ref_df = refs.ref_gen().df
    logger.error("Refs:{}".format(ref_df))
    # Ref model initialization data
    from json import dumps
    ref_df['Tags'] = ref_df['Tags'].apply(dumps)
    ref_df['Jobs'] = ref_df['Jobs'].apply(dumps)
    ref_df['Features'] = ref_df['Features'].apply(dumps)
    return ref_df

def get_recent_jobs():
    import jobs
    return jobs.job_gen().df

# Check if string time has 1 or 2 colons and convert grabbing just time
def conv_str_time(st):
    logger.info("Convert to time")
    import datetime
    if st.count(':') == 2:
        return datetime.datetime.strptime(q[1][1],"%H:%M:%S").time()
    elif st.count(':') == 1:
        return datetime.datetime.strptime(q[1][1],"%H:%M").time()
    else:
        return None
