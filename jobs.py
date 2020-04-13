""" jobs
methods for converting and displaying jobs in dash
"""

from logging import getLogger
import pandas as pd
import numpy as np
import dash_config
logger = getLogger(__name__)  # pylint: disable=invalid-name

# if (__name__ != "__main__"):
if dash_config.MOCK_EPMT_API:
    import epmt_query_mock as eq
else:
    import epmt_query as eq


class JobGen:
    """JobGen class:
    holds job dataframe after converting fields to display
    """
    def __init__(self, jobs=[], limit=30, offset=0):
        if jobs:
            logger.debug("Jobs requested {}".format(jobs))
        sample = None
        errmsg = None
        try:
            sample = eq.get_jobs(jobs=jobs, fmt='dict', limit=limit, offset=offset)
        except Exception as E:
            logger.error("Job with ID:\"{}\", Not Found or broken".format(E))
            # If debug mode assign the error to the dataframe second column
            if dash_config.DEBUG:
                errmsg = E
        
        if sample:
            self.jobs_df = pd.DataFrame(sample)
            self.jobs_df = self.jobs_df.sort_values(
                "start",  # Column to sort on
                ascending=False,  # Boolean eval.
                inplace=False
            )
            # Extract the exit code to a column
            exit_codes = [d.get('status')['exit_code']
                          for d in self.jobs_df.info_dict]
            self.jobs_df['exit_code'] = exit_codes
            self.jobs_df['Processed'] = 0
            ## Extract tags out and merge them in as columns
            #tags = pd.DataFrame.from_dict(self.jobs_df['tags'].tolist())
            #self.jobs_df = pd.merge(self.jobs_df,tags, left_index=True, right_index=True)
            #self.jobs_df.drop('tags', axis=1)
            #pd.set_option('display.max_rows', None)
            #pd.set_option('display.max_columns', None)
            #pd.set_option('display.width', None)
            #pd.set_option('display.max_colwidth', -1)
            #self.jobs_df = self.jobs_df[dash_config.columns_to_print]
            #logger.debug("df {}".format(self.jobs_df))

            # Convert Job date into a start_day datetime date
            self.jobs_df['start_day'] = self.jobs_df.start.map(lambda x: x.date())
            # datetime.strptime(start, "%Y-%m-%d").date()

            # Select specific tags for displaying
            # logger.info("Tags{}".format(self.jobs_df['tags']))

            # Convert True into 'Yes' for user friendly display
            self.jobs_df['Processed'] = np.where(self.jobs_df['Processed'], 'Yes', 'No')
            self.jobs_df = self.jobs_df[dash_config.columns_to_print]
            # User friendly column names
            self.jobs_df.rename(columns={
                'jobid': 'job id',
                'exit_code': 'exit status',
                'Processed': 'processing complete',
                'write_bytes': 'bytes_out',
                'read_bytes': 'bytes_in'
            }, inplace=True)
        else:
            self.jobs_df = pd.DataFrame([["No Jobs ", str(errmsg) if errmsg else None]] , columns=['job id','exit status'])
            self.jobs_df.append(pd.Series(), ignore_index=True)
            logger.debug(
                "No jobs found here is an empty jobs_df\n%s", self.jobs_df)

# ####################### End List of jobs ########################


JOBS_DF = pd.DataFrame()


def get_version():
    """Returns a mock version
    """
    return "EPMT 1.1.1"
