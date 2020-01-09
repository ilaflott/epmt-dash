# Generate a random list of jobs
from string import ascii_letters
import random
import datetime
import time
import pandas as pd

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

#if (__name__ != "__main__"):
from pathlib import Path
curdir = Path.cwd().stem
if (curdir == "ui"):
    import epmt_query_mock as eq
else:
    import epmt_query as eq



# Job_gen does data cleanup and conversions for displaying
class job_gen:
    def __init__(self, limit=60, offset=0):
        from dash_config import columns_to_print
        sample = eq.get_jobs(fmt='dict', limit=limit, offset=offset)
        if sample:
            self.df = pd.DataFrame(sample)
            self.df = self.df.sort_values(
                    "start",  # Column to sort on
                    ascending = False,  # Boolean eval.
                    inplace=False
                )
            # Extract the exit code to a column
            exit_codes = [d.get('status')['exit_code'] for d in self.df.info_dict]
            self.df['exit_code'] = exit_codes
            self.df['Processed'] = 0
            # Extract tags out and merge them in as columns
            # tags = pd.DataFrame.from_dict(self.df['tags'].tolist())
            # self.df = pd.merge(self.df,tags, left_index=True, right_index=True)

            # Convert Job date into a start_day datetime date
            self.df['start_day'] = self.df.start.map(lambda x: x.date())
            # datetime.strptime(start, "%Y-%m-%d").date()

            # Select specific tags for displaying
            # logger.info("Tags{}".format(self.df['tags']))

            # Convert True into 'Yes' for user friendly display
            import numpy as np
            self.df['Processed'] = np.where(self.df['Processed'], 'Yes', 'No')
        else:
            self.df = pd.DataFrame(columns=columns_to_print)
            self.df.append(pd.Series(), ignore_index=True)
            logger.debug("No jobs found here is an empty df\n{}".format(self.df))

        self.df = self.df[columns_to_print]
        
        # User friendly column names
        self.df.rename(columns={
            'jobid': 'job id',
            'exit_code': 'exit status',
            'Processed': 'processing complete',
            'write_bytes': 'bytes_out',
            'read_bytes': 'bytes_in'
        }, inplace=True)

# ####################### End List of jobs ########################



# API Call
def detect_outlier_jobs(jobs, trained_model=None, features=['cpu_time', 'duration', 'num_procs'], methods=['modified_z_score'], thresholds='thresholds', sanity_check=True):
    """
    (df, parts) = eod.detect_outlier_jobs(jobs)
    pprint(parts)
    {'cpu_time': ([u'kern-6656-20190614-190245',
                   u'kern-6656-20190614-194024',
                   u'kern-6656-20190614-191138'],
                  [u'kern-6656-20190614-192044-outlier']),
     'duration': ([u'kern-6656-20190614-190245',
                   u'kern-6656-20190614-194024',
                   u'kern-6656-20190614-191138'],
                  [u'kern-6656-20190614-192044-outlier']),
     'num_procs': ([u'kern-6656-20190614-190245',
                    u'kern-6656-20190614-192044-outlier',
                    u'kern-6656-20190614-194024',
                    u'kern-6656-20190614-191138'],
                   [])}
    """
    returns = ('df', {'feature' : (['job','job2'], ['joboutlier'])})
    return "Running outlier analysis on Jobs: " + str(jobs)

df = pd.DataFrame()

def get_version():
    return "EPMT 1.1.1"
