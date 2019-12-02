import pandas as pd
import numpy as np

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name


#
def make_refs(x,name='',jobs=None):
    from jobs import get_recent_jobs
    job_df = get_recent_jobs()
    from random import randint,getrandbits

    refs = []
    joblist = job_df['job id'].sample(n = 1).tolist()
    featureli = ['duration','cpu_time','num_procs']
    #print(joblist)

    for n in range(x):
        if not jobs:
            jobs = [ joblist[i] for i in range(randint(1,1))]         #  setup 5-8 jobs per ref
        features = [featureli[i] for i in range(randint(1,3))]    #  Setup random features
        ref_active = bool(getrandbits(1)  < 0.95)                 #  95% Chance of being active
        refs.append(['ref'+str(n)+name, {"taga":"tagb"}, jobs,
                     features, ref_active])                       # Append each ref to refs list
    return refs

# Generate a list of references
class ref_gen:
    def __init__(self):
        references = make_refs(3)
        self.df = pd.DataFrame(references, columns=['Model','Tags','Jobs','Features','Active'])
        self.df['Active'] = np.where(self.df['Active'], 'Yes', 'No')
        # Reorder
        self.df = self.df[['Model','Active','Tags','Jobs','Features']]


# Grabs sample reference models
# formats them
# returns dataframe
def get_references():
    ref_df = ref_gen().df
    logger.debug("Refs({}):\n{}".format(id(ref_df),ref_df))
    # Ref model initialization data
    from json import dumps
    ref_df['Tags'] = ref_df['Tags'].apply(dumps) # Dumps stringify's dictionaries
    ref_df['Jobs'] = ref_df['Jobs'].apply(dumps) # Dumps stringify's lists
    ref_df['Features'] = ref_df['Features'].apply(dumps) # Dumps stringify's lists
    return ref_df