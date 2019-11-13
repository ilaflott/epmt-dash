# Generate a random list of jobs
import random
import pandas as pd
from string import ascii_letters
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

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
        Processed = bool(random.getrandbits(1))
        tag = dict(tags) if bool(random.getrandbits(1)) else {'Tags':'None'}
        usert = random.randrange(0,8640000*0.5)
        systemt = random.randrange(0,8640000*0.5)
        cput = usert+systemt
        duration = random.uniform(cput, cput*1.3) # 8640000 jiffies in 24 hours

        result.append([jobid,Processed,tag,
             # Exit code, duration, user, system
             random.getrandbits(1),duration,usert,systemt,cput,
             # Bytes in, Bytes out
             random.randrange(0,1024**4),random.randrange(0,1024**4)])
    return result

df = pd.DataFrame()
class job_gen:
  def __init__(self):
    sample = make_jobs(20)
    # Here tags are excluded as the datatable doesn't support dictionaries
    self.df = pd.DataFrame(sample, columns=['jobid','Processed','tags','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out'])
    from json import dumps
    self.df['tags'] = self.df['tags'].apply(dumps)
    #logger.info("Tags{}".format(self.df['tags']))
    self.df = self.df[['jobid','Processed','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out','tags']]
    import numpy as np
    self.df['Processed'] = np.where(self.df['Processed'], 'Yes', 'No')
    # Useful Renaming
    self.df.rename(columns={
      'jobid': 'Job ID',
      'duration':'Duration (HH:MM:SS)',
      'Processed': 'Processing Complete',
      'exit_code': 'Exit Status'
        }, inplace=True)
  def reset(self):
    self.__init__()

#unproc_df = df.loc[df['Processing Complete'] == True].to_dict('records')
    
######################## End List of jobs ########################

def get_version():
  return "EPMT 1.1.1"