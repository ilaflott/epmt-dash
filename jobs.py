# Generate a random list of jobs
import random
import pandas as pd
from string import ascii_letters
tags = {'atm_res': 'c96l49',
   'ocn_res': '0.5l75',
   'exp_name': 'ESM4_historical_D151',
   'exp_time': '18640101',
   'script_name': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18640101',
   'exp_component': 'ocean_annual_rho2_1x1deg'}
def make_jobs(x):
    result = []
    for n in range(x):
        usert = random.randrange(0,352347842)
        systemt = random.randrange(0,138302869)
        cput = usert+systemt
        duration = random.uniform(cput, cput*1.3)
        result.append(["job-"+str(n),bool(random.getrandbits(1)),dict(tags) if bool(random.getrandbits(1)) else None,
             # Exit code, duration, user, system
             random.getrandbits(1),duration,usert,systemt,cput,
             # Bytes in, Bytes out
             random.randrange(0,632651776),random.randrange(0,632651776)])
    return result


sample = make_jobs(8)

# Here tags are excluded as the datatable doesn't support dictionaries
df = pd.DataFrame(sample, columns=['jobid','Processed','tags','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out'])
df = df[['jobid','Processed','exit_code','duration','usertime','systemtime','cpu_time','bytes_in','bytes_out']]
import numpy as np
# Bools don't show in dash datatable
# https://github.com/plotly/dash-table-experiments/issues/10
df['Processed'] = np.where(df['Processed'], 'Yes', 'No')
# Useful Renaming
df.rename(columns={
  'jobid': 'Job ID',
  'Processed': 'Processing Complete',
  'exit_code': 'Exit Status'
    }, inplace=True)
#unproc_df = df.loc[df['Processing Complete'] == True].to_dict('records')
    
######################## End List of jobs ########################