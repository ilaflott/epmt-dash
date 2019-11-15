# Generate a random list of jobs
import random
import time
import pandas as pd
from string import ascii_letters
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, dfmt, prop):
    return str_time_prop(start, end, dfmt, prop)


# Generate Random time,zone
# random_date("1:30 PM UTC", "4:50 PM UTC", "%I:%M %p %Z", random.random())
# Generate Random Date,time,zone
# random_date("1/1/1990 1:30 PM UTC", "1/2/1990 4:50 PM UTC", "%m/%d/%Y %I:%M %p %Z", random.random())

tags = {'atm_res': 'c96l49',
   'ocn_res': '0.5l75',
   'exp_name': 'ESM4_historical_D151',
   'exp_time': '18640101',
   'script_name': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18640101',
   'exp_component': 'ocean_annual_rho2_1x1deg'}
def make_jobs(x):
    result = []
    for n in range(x):
        jobid = "job-"+str(n)
        import names
        job_name = names.name_gen().name
        Processed = bool(random.getrandbits(1))
        tag = dict(tags) if bool(random.getrandbits(1)) else {'Tags':'None'}
        start_time = random_date("1:30 PM UTC", "4:50 PM UTC", "%I:%M %p %Z", random.random())
        usert = random.randrange(0,8640000*0.5)
        systemt = random.randrange(0,8640000*0.5)
        cput = usert+systemt
        duration = random.uniform(cput, cput*1.3) # 8640000 jiffies in 24 hours
        exit_code = 1 if bool(random.random() < 0.3) else 0
        result.append([jobid,job_name,Processed,tag, start_time,
             # Exit code, duration, user, system
             exit_code, duration,usert,systemt,cput,
             # Bytes in, Bytes out
             random.randrange(0,1024**4),random.randrange(0,1024**4)])
    return result

df = pd.DataFrame()
class job_gen:
  def __init__(self):
    sample = make_jobs(20)
    # Here tags are excluded as the datatable doesn't support dictionaries
    self.df = pd.DataFrame(sample, columns=['jobid','name','Processed','tags','start_time','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out'])
    from json import dumps
    self.df['tags'] = self.df['tags'].apply(dumps)
    #logger.info("Tags{}".format(self.df['tags']))
    self.df = self.df[['jobid','name','start_time','Processed','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out','tags']]
    import numpy as np
    self.df['Processed'] = np.where(self.df['Processed'], 'Yes', 'No')
    # Useful Renaming
    self.df.rename(columns={
      'jobid': 'job id',
      'duration':'duration (HH:MM:SS)',
      'Processed': 'processing complete',
      'exit_code': 'exit status'
        }, inplace=True)
  def reset(self):
    self.__init__()

#unproc_df = df.loc[df['Processing Complete'] == True].to_dict('records')
    
######################## End List of jobs ########################

def get_version():
  return "EPMT 1.1.1"