""" jobs
methods for converting and displaying jobs in dash
"""

from logging import getLogger
from pathlib import Path
import pandas as pd
import numpy as np
from dash_config import columns_to_print
logger = getLogger(__name__)  # pylint: disable=invalid-name

# if (__name__ != "__main__"):
if Path.cwd().stem == "ui":
    import epmt_query_mock as eq
else:
    import epmt_query as eq


class JobGen:
    """JobGen class:
    holds job dataframe after converting fields to display
    """
    def __init__(self, limit=60, offset=0):
        sample = eq.get_jobs(fmt='dict', limit=limit, offset=offset)
        if sample:
            self.df = pd.DataFrame(sample)
            self.df = self.df.sort_values(
                "start",  # Column to sort on
                ascending=False,  # Boolean eval.
                inplace=False
            )
            # Extract the exit code to a column
            exit_codes = [d.get('status')['exit_code']
                          for d in self.df.info_dict]
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
            self.df['Processed'] = np.where(self.df['Processed'], 'Yes', 'No')
        else:
            self.df = pd.DataFrame(columns=columns_to_print)
            self.df.append(pd.Series(), ignore_index=True)
            logger.debug(
                "No jobs found here is an empty df\n{}".format(self.df))

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


df = pd.DataFrame()


def get_version():
    """Returns a mock version
    """
    return "EPMT 1.1.1"
