import pandas as pd
import numpy as np
import datetime

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name


# Mock sample
# get_ref returns
def get_ref():
    get_ref = [{'tags': {},
                'updated_at': None,
                'created_at': datetime.datetime(2019, 11, 26, 22, 53, 42, 447548),
                'info_dict': None,
                'id': 1,
                'op_tags': [],
                'enabled': True,
                'jobs': ['685000', '685003', '685016'],
                'modified_z_score': {'duration': [1.6944, 6615525773.0, 155282456.0],
                                    'num_procs': [3.0253, 3480.0, 68.0],
                                    'cpu_time': [10.8055, 113135329.0, 19597296.0]}}]
    return get_ref


# API Call
def create_refmodel(jobs=[], name=None, tag={}, op_tags=[],
                    outlier_methods=["modified_z_score"],
                    features=['duration', 'cpu_time', 'num_procs'], exact_tag_only=False,
                    fmt='dict', sanity_check=True, enabled=True):
    create_ref = {'jobs': jobs,
                  'tags': {},
                  'op_tags': [],
                  'computed': {'modified_z_score': {'duration': (1.6944,
                                                                 6615525773.0,
                                                                 155282456.0),
                                                    'num_procs': (3.0253, 3480.0, 68.0),
                                                    'cpu_time': (10.8055, 113135329.0, 19597296.0)}},
                  'enabled': True,
                  'id': 1,
                  'created_at': datetime.datetime(2019, 11, 26, 22, 53, 42, 447548)}
    return create_ref

def make_refs(name='', jobs=None, tags={}):
    import sys
    sys.path.append("./..")
    logger.debug(sys.path)
    import epmt_query as eq
    # eq.create_refmodel(jobs=['625133','693118','696085'], name='Sample', tag={'exp_name':'ESM4_historical_D151','exp_component': 'atmos_cmip'})
    nm = eq.create_refmodel(jobs=jobs, name=name, tag=tags)
    return [nm['name'], nm['created_at'], nm['tags'], nm['jobs'], 'duration', nm['enabled']]

# Returns a list of model data to be converted into a dataframe
def _old_make_refs(x, name='', jobs=None, tags={}):
    from random import randint, getrandbits
    from jobs import job_gen
    # Our generated references need to pull jobids and tags from jobs
    job_df = job_gen().df
    refs = []
    joblist = job_df['job id'].tolist()
    featureli = ['duration', 'cpu_time', 'num_procs']
    datefmt = "%Y-%m-%d"
    from copy import deepcopy
    for n in range(x):
        # If jobs were not passed randomly create some 500 days ago
        # subsequent jobs will be incrementally sooner
        from datetime import date, timedelta
        ref_date = (date.today() - timedelta(days=500) +
                    timedelta(days=n)).strftime(datefmt)
        if not jobs:
            ref_jobs = [joblist[i]
                        for i in range(randint(1, 1))]  # setup 5-8 jobs per ref
            # 95% Chance of being active
            ref_active = False
            features = [featureli[i]
                        for i in range(randint(1, 3))]  # Setup random features
            jname = 'Sample_Model_' + str(n) + name
            tags = {"exp_name": "ESM0_historical", "exp_component": "ocean_annual_rho2_1x1deg"}
        else:
            # User is building a reference with jobs selected today
            jname = name
            ref_jobs = jobs
            today = date.today()
            # Ref model is being generated now
            ref_date = today.strftime(datefmt)
            ref_active = True   # Set active User Friendly
            features = featureli  # Full Features
        refs.append(deepcopy([jname, ref_date, tags, ref_jobs,
                     features, ref_active]))                       # Append each ref to refs list
    return refs

# Generate a list of sample references
# ref_gen does data cleanup and conversions for displaying reference models
class ref_gen:
    def __init__(self):
        #references = make_refs(2)
        self.df = pd.DataFrame([], columns=[
                               'name', 'date created', 'tags', 'jobs', 'features', 'active'])
        # self.df['active'] = np.where(self.df['active'], 'Yes', 'No')
        # Reorder
        self.df = self.df[['name', 'active',
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


ref_df = get_references()
