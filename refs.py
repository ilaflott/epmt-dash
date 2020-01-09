import pandas as pd
import numpy as np
import datetime

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

# if (__name__ != "__main__"):
from pathlib import Path
curdir = Path.cwd().stem
if (curdir == "ui"):
    import epmt_query_mock as eq
else:
    import epmt_query as eq


def get_refs():
    m = eq.get_refmodels()
    return [[nm['id'], nm['name'], nm['created_at'], nm['tags'], nm['jobs'], ['duration', 'cpu_time', 'num_procs'], nm['enabled']] for nm in m]


def make_refs(name='', jobs=None, tags={}, active=True):
    # eq.create_refmodel(jobs=['625133','693118','696085'], name='Sample', tag={'exp_name':'ESM4_historical_D151','exp_component': 'atmos_cmip'})
    try:
        nm = eq.create_refmodel(jobs=jobs, name=name, tag=tags, enabled=active)
        return [[nm['id'], nm['name'], nm['created_at'], nm['tags'], nm['jobs'], ['duration', 'cpu_time', 'num_procs'], nm['enabled']]]
    except Exception as e:
        logger.error("Create model failed {}".format(e))
        return None

# Generate a list of sample references
# ref_gen does data cleanup and conversions for displaying reference models
class ref_gen:
    def __init__(self):
        #references = make_refs(2)
        self.df = pd.DataFrame(get_refs(), columns=['id',
                               'name', 'date created', 'tags', 'jobs', 'features', 'active'])
        # self.df['active'] = np.where(self.df['active'], 'Yes', 'No')
        # Reorder
        self.df = self.df[['id', 'name', 'active',
                           'date created', 'tags', 'jobs', 'features']]


# Grabs sample reference models
# formats them
# returns dataframe
def get_references():
    ref_df = ref_gen().df
    logger.debug("Refs({}):\n{}".format(id(ref_df), ref_df))
    # Ref model initialization data
    from json import dumps
    ref_df['tags'] = ref_df['tags'].apply(dumps)  # Dumps stringify's dictionaries
    ref_df['jobs'] = ref_df['jobs'].apply(dumps)  # Dumps stringify's lists
    ref_df['features'] = ref_df['features'].apply(
        dumps)  # Dumps stringify's lists
    return ref_df

# Accepts primary key model_name and new jobs
# Deletes original model then creates new one
# Returns ID of new model
def edit_model(model_name, new_jobs, del_original=True):
    orig_model = eq.get_refmodels(model_name)[0]
    mname = orig_model['name']
    mid = orig_model['id']
    mtags = orig_model['tags']
    menabled = orig_model['enabled']
    mjobs = new_jobs

    if del_original:
        eq.delete_refmodels(mid)
    ret = make_refs(name=mname, jobs=mjobs, tags=mtags,active=menabled)
    return ret[0][0]
    

ref_df = get_references()
