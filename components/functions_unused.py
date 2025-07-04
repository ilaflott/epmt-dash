""" Methods previously used for random job generation
"""
# pylint: disable-all

from datetime import date, timedelta

def str_time_prop(start, end, format):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

# Check if string time has 1 or 2 colons and convert grabbing just time
def conv_str_time(st):
    logger.info("Convert to time")
    import datetime
    if st.count(':') == 1:
        return datetime.datetime.strptime(st[1][1],"%H:%M").time()
    # limit functionality for now
    #if st.count(':') == 2:
    #    return datetime.datetime.strptime(st[1][1],"%H:%M:%S").time()
    else:
        return None

def random_date(start, end, dfmt):
    return str_time_prop(start, end, dfmt)
# Generate Random time,zone
# random_date("1:30 PM UTC", "4:50 PM UTC", "%I:%M %p %Z", random.random())
# Generate Random Date,time,zone
# random_date("1/1/1990 1:30 PM UTC", "1/2/1990 4:50 PM UTC", "%m/%d/%Y %I:%M %p %Z", random.random())


def _unused_random_JobGenerator(x):
    # Old tags
    tags = {'atm_res': 'c96l49',
            'ocn_res': '0.5l75',
            'exp_name': 'ESM4_historical_D151',
            'exp_time': '18640101',
            'script_name': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18640101',
            'exp_component': 'ocean_annual_rho2_1x1deg'}
    result = []
    for n in range(x):
        jobid = "job-" + str(n)
        from .. import names
        job_name = names.name_gen().name
        Processed = bool(random.getrandbits(1))
        tag = dict(tags) if bool(random.getrandbits(1)) else {'Tags': 'None'}
        timeformat = "%m/%d/%Y %I:%M %p %Z"
        start_datetime = random_date(
            "11/1/2019 1:30 PM UTC", "11/5/2019 4:50 PM UTC", timeformat)  # + timedelta(days=n)
        from datetime import datetime
        start_time = datetime.strptime(start_datetime, timeformat).time()
        start_day = datetime.strptime(start_datetime, timeformat).date()
        usert = random.randrange(0, 8640000 * 0.5)
        systemt = random.randrange(0, 8640000 * 0.5)
        cput = usert + systemt
        # 8640000 jiffies in 24 hours
        duration = random.uniform(cput, cput * 1.3)
        exit_code = int(1) if bool(random.random() < 0.3) else int(0)
        result.append([jobid, job_name, Processed, tag, start_day, start_time,
                       # Exit code, duration, user, system
                       exit_code, duration, usert, systemt, cput,
                       # Bytes in, Bytes out
                       random.randrange(0, 1024**4), random.randrange(0, 1024**4)])
    return result

    def reset(self):
        self.__init__()


# Returns a list of model data to be converted into a dataframe
def _old_make_refs(x, name='', jobs=None, tags={}):
    from random import randint, getrandbits
    from .. import Jobs as j
    # Our generated references need to pull jobids and tags from jobs
    job_df = j.JobGen().jobs_df
    refs = []
    joblist = job_df['job id'].tolist()
    featureli = ['duration', 'cpu_time', 'num_procs']
    datefmt = "%Y-%m-%d"
    from copy import deepcopy
    for n in range(x):
        # If jobs were not passed randomly create some 500 days ago
        # subsequent jobs will be incrementally sooner
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

from string import ascii_letters
import random
import datetime
import time
import pandas as pd

samplej = {'duration': 6460243317.0,
           'updated_at': datetime.datetime(2019, 11, 26, 22, 0, 22, 485979),
           'tags': {'exp_name': 'ESM4_historical_D151',
                    'exp_component': 'ocean_annual_rho2_1x1deg',
                    'exp_time': '18840101',
                    'atm_res': 'c96l49',
                    'ocn_res': '0.5l75',
                    'script_name': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101'},
           'info_dict': {'tz': 'US/Eastern',
                         'status': {'exit_code': 0,
                                    'exit_reason': 'none',
                                    'script_path': '/home/Jeffrey.Durachta/ESM4/DECK/ESM4_historical_D151/gfdl.ncrc4-intel16-prod-openmp/scripts/postProcess/ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101.tags',
                                    'script_name': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101'}},
           'env_dict': {'TMP': '/vftmp/Jeffrey.Durachta/job685000',
                        'MODULE_VERSION': '3.2.10',
                        'GROUP': 'f',
                        'SLURM_SUBMIT_DIR': '/home/Jeffrey.Durachta/ESM4/DECK/ESM4_historical_D151/gfdl.ncrc4-intel16-prod-openmp/scripts/postProcess',
                        'SLURM_NODEID': '0',
                        'SLURM_JOBID': '685000',
                        'HOSTTYPE': 'x86_64-linux',
                        'ENVIRONMENT': 'BATCH',
                        'MODULESHOME': '/usr/local/Modules/3.2.10',
                        'SLURM_LOCALID': '0',
                        'LOGNAME': 'Jeffrey.Durachta',
                        'USER': 'Jeffrey.Durachta',
                        'HOME': '/home/Jeffrey.Durachta',
                        'PATH': '/home/gfdl/bin2:/usr/local/bin:/bin:/usr/bin:.',
                        'SLURM_JOB_NODELIST': 'pp208',
                        'SLURM_JOB_USER': 'Jeffrey.Durachta',
                        'LANG': 'en_US',
                        'TERM': 'dumb',
                        'SHELL': '/bin/tcsh',
                        'SLURM_JOB_CPUS_PER_NODE': '1',
                        'SHLVL': '2',
                        'SLURM_JOB_QOS': 'Added as default',
                        'SLURM_JOB_UID': '4067',
                        'SLURM_GET_USER_ENV': '1',
                        'SLURM_NODELIST': 'pp208',
                        'pp_script': '/home/Jeffrey.Durachta/ESM4/DECK/ESM4_historical_D151/gfdl.ncrc4-intel16-prod-openmp/scripts/postProcess/ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101.tags',
                        'PAPIEX_OUTPUT': '/vftmp/Jeffrey.Durachta/job685000/papiex/',
                        'SLURM_JOB_NUM_NODES': '1',
                        'MANPATH': '/home/gfdl/man:/usr/local/man:/usr/share/man',
                        'SLURM_PROCID': '0',
                        'OSTYPE': 'linux',
                        'SLURM_TASKS_PER_NODE': '1',
                        'HOSTNAME': 'pp208',
                        'ARCHIVE': '/archive/Jeffrey.Durachta',
                        'SLURM_SUBMIT_HOST': 'an104',
                        'VENDOR': 'unknown',
                        'JOB_ID': '685000',
                        'MODULE_VERSION_STACK': '3.2.10',
                        'SLURM_CLUSTER_NAME': 'gfdl',
                        'jobname': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101',
                        'SLURM_JOB_PARTITION': 'batch',
                        'HOST': 'pp208',
                        'SLURM_JOB_ID': '685000',
                        'SLURM_NTASKS': '1',
                        'SLURM_NODE_ALIASES': '(null)',
                        'SLURM_CPUS_ON_NODE': '1',
                        'LOADEDMODULES': '',
                        'SLURM_JOB_GID': '70',
                        'TMPDIR': '/vftmp/Jeffrey.Durachta/job685000',
                        'MODULEPATH': '/usr/local/Modules/modulefiles:/home/fms/local/modulefiles',
                        'EPMT': '/home/Jeffrey.Durachta/workflowDB/build//epmt/epmt',
                        'SLURM_NPROCS': '1',
                        'EPMT_JOB_TAGS': 'exp_name:ESM4_historical_D151;exp_component:ocean_annual_rho2_1x1deg;exp_time:18840101;atm_res:c96l49;ocn_res:0.5l75;script_name:ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101',
                        'SLURM_PRIO_PROCESS': '0',
                        'OMP_NUM_THREADS': '1',
                        'SLURM_CHECKPOINT_IMAGE_DIR': '/var/slurm/checkpoint',
                        'SLURM_GTIDS': '0',
                        'SLURM_TASK_PID': '6089',
                        'SLURM_NNODES': '1',
                        'SLURM_JOB_NAME': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101',
                        'SLURM_TOPOLOGY_ADDR': 'pp208',
                        'PWD': '/vftmp/Jeffrey.Durachta/job685000',
                        'SLURM_TOPOLOGY_ADDR_PATTERN': 'node',
                        'WORKFLOWDB_PATH': '/home/Jeffrey.Durachta/workflowDB/build/',
                        'SLURM_JOB_ACCOUNT': 'gfdl_f',
                        'LC_TIME': 'C',
                        'MACHTYPE': 'x86_64',
                        'SLURMD_NODENAME': 'pp208',
                        'SLURM_WORKING_CLUSTER': 'gfdl:slurm01:6817:8448'},
           'cpu_time': 113135329.0,
           'annotations': {},
           'env_changes_dict': {},
           'analyses': {},
           'submit': datetime.datetime(2019, 6, 15, 7, 52, 4, 73965),
           'start': datetime.datetime(2019, 6, 15, 7, 52, 4, 73965),
           'jobid': 'job1',
           'end': datetime.datetime(2019, 6, 15, 9, 39, 44, 317282),
           'jobname': 'ESM4_historical_D151_ocean_annual_rho2_1x1deg_18840101',
           'created_at': datetime.datetime(2019, 11, 26, 22, 0, 8, 937521),
           'exitcode': 0,
           'user': 'Jeffrey.Durachta',
           'all_proc_tags': [{'op': 'cp', 'op_instance': '11', 'op_sequence': '66'},
                             {'op': 'cp', 'op_instance': '15', 'op_sequence': '79'},
                             {'op': 'cp', 'op_instance': '3', 'op_sequence': '30'},
                             {'op': 'cp', 'op_instance': '5', 'op_sequence': '39'},
                             {'op': 'cp', 'op_instance': '7', 'op_sequence': '48'},
                             {'op': 'cp', 'op_instance': '9', 'op_sequence': '57'},
                             {'op': 'dmput', 'op_instance': '2',
                                 'op_sequence': '89'},
                             {'op': 'fregrid', 'op_instance': '2',
                                 'op_sequence': '31'},
                             {'op': 'fregrid', 'op_instance': '3',
                                 'op_sequence': '40'},
                             {'op': 'fregrid', 'op_instance': '4',
                                 'op_sequence': '49'},
                             {'op': 'fregrid', 'op_instance': '5',
                                 'op_sequence': '58'},
                             {'op': 'fregrid', 'op_instance': '6',
                                 'op_sequence': '67'},
                             {'op': 'fregrid', 'op_instance': '7',
                                 'op_sequence': '80'},
                             {'op': 'hsmget', 'op_instance': '1', 'op_sequence': '1'},
                             {'op': 'hsmget', 'op_instance': '1', 'op_sequence': '3'},
                             {'op': 'hsmget', 'op_instance': '1', 'op_sequence': '5'},
                             {'op': 'hsmget', 'op_instance': '1', 'op_sequence': '7'},
                             {'op': 'hsmget', 'op_instance': '1', 'op_sequence': '9'},
                             {'op': 'hsmget', 'op_instance': '3',
                                 'op_sequence': '10'},
                             {'op': 'hsmget', 'op_instance': '3', 'op_sequence': '2'},
                             {'op': 'hsmget', 'op_instance': '3', 'op_sequence': '4'},
                             {'op': 'hsmget', 'op_instance': '3', 'op_sequence': '6'},
                             {'op': 'hsmget', 'op_instance': '3', 'op_sequence': '8'},
                             {'op': 'hsmget', 'op_instance': '4',
                                 'op_sequence': '11'},
                             {'op': 'hsmget', 'op_instance': '4',
                                 'op_sequence': '14'},
                             {'op': 'hsmget', 'op_instance': '4',
                                 'op_sequence': '17'},
                             {'op': 'hsmget', 'op_instance': '4',
                                 'op_sequence': '20'},
                             {'op': 'hsmget', 'op_instance': '4',
                                 'op_sequence': '23'},
                             {'op': 'hsmget', 'op_instance': '6',
                                 'op_sequence': '12'},
                             {'op': 'hsmget', 'op_instance': '6',
                                 'op_sequence': '15'},
                             {'op': 'hsmget', 'op_instance': '6',
                                 'op_sequence': '18'},
                             {'op': 'hsmget', 'op_instance': '6',
                                 'op_sequence': '21'},
                             {'op': 'hsmget', 'op_instance': '6',
                                 'op_sequence': '24'},
                             {'op': 'hsmget', 'op_instance': '7',
                                 'op_sequence': '13'},
                             {'op': 'hsmget', 'op_instance': '7',
                                 'op_sequence': '16'},
                             {'op': 'hsmget', 'op_instance': '7',
                                 'op_sequence': '19'},
                             {'op': 'hsmget', 'op_instance': '7',
                                 'op_sequence': '22'},
                             {'op': 'hsmget', 'op_instance': '7',
                                 'op_sequence': '25'},
                             {'op': 'mv', 'op_instance': '1', 'op_sequence': '33'},
                             {'op': 'mv', 'op_instance': '10', 'op_sequence': '60'},
                             {'op': 'mv', 'op_instance': '13', 'op_sequence': '69'},
                             {'op': 'mv', 'op_instance': '16', 'op_sequence': '74'},
                             {'op': 'mv', 'op_instance': '18', 'op_sequence': '83'},
                             {'op': 'mv', 'op_instance': '18', 'op_sequence': '86'},
                             {'op': 'mv', 'op_instance': '20', 'op_sequence': '84'},
                             {'op': 'mv', 'op_instance': '20', 'op_sequence': '87'},
                             {'op': 'mv', 'op_instance': '4', 'op_sequence': '42'},
                             {'op': 'mv', 'op_instance': '7', 'op_sequence': '51'},
                             {'op': 'ncatted', 'op_instance': '11',
                                 'op_sequence': '68'},
                             {'op': 'ncatted', 'op_instance': '12',
                                 'op_sequence': '73'},
                             {'op': 'ncatted', 'op_instance': '15',
                                 'op_sequence': '82'},
                             {'op': 'ncatted', 'op_instance': '15',
                                 'op_sequence': '85'},
                             {'op': 'ncatted', 'op_instance': '3',
                                 'op_sequence': '32'},
                             {'op': 'ncatted', 'op_instance': '5',
                                 'op_sequence': '41'},
                             {'op': 'ncatted', 'op_instance': '7',
                                 'op_sequence': '50'},
                             {'op': 'ncatted', 'op_instance': '9',
                                 'op_sequence': '59'},
                             {'op': 'ncrcat', 'op_instance': '10',
                                 'op_sequence': '62'},
                             {'op': 'ncrcat', 'op_instance': '12',
                                 'op_sequence': '71'},
                             {'op': 'ncrcat', 'op_instance': '13',
                                 'op_sequence': '76'},
                             {'op': 'ncrcat', 'op_instance': '2',
                                 'op_sequence': '26'},
                             {'op': 'ncrcat', 'op_instance': '4',
                                 'op_sequence': '35'},
                             {'op': 'ncrcat', 'op_instance': '6',
                                 'op_sequence': '44'},
                             {'op': 'ncrcat', 'op_instance': '8',
                                 'op_sequence': '53'},
                             {'op': 'rm', 'op_instance': '1', 'op_sequence': '27'},
                             {'op': 'rm', 'op_instance': '10', 'op_sequence': '54'},
                             {'op': 'rm', 'op_instance': '11', 'op_sequence': '61'},
                             {'op': 'rm', 'op_instance': '13', 'op_sequence': '63'},
                             {'op': 'rm', 'op_instance': '14', 'op_sequence': '70'},
                             {'op': 'rm', 'op_instance': '16', 'op_sequence': '75'},
                             {'op': 'rm', 'op_instance': '18', 'op_sequence': '77'},
                             {'op': 'rm', 'op_instance': '19', 'op_sequence': '88'},
                             {'op': 'rm', 'op_instance': '2', 'op_sequence': '34'},
                             {'op': 'rm', 'op_instance': '4', 'op_sequence': '36'},
                             {'op': 'rm', 'op_instance': '5', 'op_sequence': '43'},
                             {'op': 'rm', 'op_instance': '7', 'op_sequence': '45'},
                             {'op': 'rm', 'op_instance': '8', 'op_sequence': '52'},
                             {'op': 'splitvars', 'op_instance': '2',
                                 'op_sequence': '81'},
                             {'op': 'timavg', 'op_instance': '1',
                                 'op_sequence': '28'},
                             {'op': 'timavg', 'op_instance': '11',
                                 'op_sequence': '72'},
                             {'op': 'timavg', 'op_instance': '3',
                                 'op_sequence': '37'},
                             {'op': 'timavg', 'op_instance': '5',
                                 'op_sequence': '46'},
                             {'op': 'timavg', 'op_instance': '7',
                                 'op_sequence': '55'},
                             {'op': 'timavg', 'op_instance': '9',
                                 'op_sequence': '64'},
                             {'op': 'untar', 'op_instance': '2',
                                 'op_sequence': '29'},
                             {'op': 'untar', 'op_instance': '3',
                                 'op_sequence': '38'},
                             {'op': 'untar', 'op_instance': '4',
                                 'op_sequence': '47'},
                             {'op': 'untar', 'op_instance': '5',
                                 'op_sequence': '56'},
                             {'op': 'untar', 'op_instance': '6',
                                 'op_sequence': '65'},
                             {'op': 'untar', 'op_instance': '7', 'op_sequence': '78'}],
           'num_procs': 3480,
           'num_threads': 3668,
           'rdtsc_duration': -112126610546481758,
           'PERF_COUNT_SW_CPU_CLOCK': 86903088007,
           'write_bytes': 12254015488,
           'systemtime': 41980075,
           'invol_ctxsw': 20900,
           'rchar': 15458131996,
           'majflt': 8,
           'guest_time': 0,
           'read_bytes': 7000064,
           'usertime': 71155254,
           'inblock': 13672,
           'rssmax': 31621528,
           'time_waiting': 10152666725,
           'outblock': 23933624,
           'user+system': 113135329,
           'wchar': 15066048420,
           'minflt': 4972187,
           'delayacct_blkio_time': 0,
           'time_oncpu': 115330986461,
           'cancelled_write_bytes': 8925798400,
           'syscr': 2182175,
           'timeslices': 795433,
           'processor': 0,
           'syscw': 897834,
           'vol_ctxsw': 770843}

# Use samplej real job as template
# replace jobid with new number
# return list of limit of jobs
#def get_jobs(limit=None, fmt='df', offset=0):
def get_jobs(jobs = [], tags=None, fltr = None, order = None, limit = None, offset = 0, when=None, before=None, after=None, hosts=[], fmt='dict', annotations=None, analyses=None, merge_proc_sums=True, exact_tag_only = False):
    from datetime import datetime, timedelta
    # if offset >= limit: offset = limit
    if offset > 0:
        # This isn't quite right..
        # df[offset:offset+limit]
        limit = offset + limit
    logger.info("Getting jobs...Limit{} Offset{}".format(limit, offset))
    sample_component = '_annual_rho2_1x1deg'
    component_list = ['ocean','land','mountian']
    sample_name = '_historical'
    name_list = ['ESM0','ESM1']
    from copy import deepcopy
    result = []
    for n in range(limit):
        job = dict(samplej)
        job['jobid'] = str(1234000 + n)
        job['Processed'] = 1
        job['start'] = job['start'] + timedelta(days=n)
        job['end'] = job['end'] + timedelta(days=n)
        name = name_list[n%2]
        job['tags']['exp_name'] = name + sample_name
        if job['jobid'] == str(1234002):
            job['tags']['exp_name'] = "mismatch_test"
        comp = component_list[n%3] + sample_component
        job['tags']['exp_component'] = str(comp)
        result.append(deepcopy(job))
    return result[offset:]

# API Call
def comparable_job_partitions(jobs, matching_keys = ['exp_name', 'exp_component']):
    # Returns [ (('matchname','matchcomponent'), {set of matchjobids}), ...]

    # Typically jobids are only passed
    # I need to get the jobids name and component
    from .jobs import job_gen
    alt = job_gen().df[job_gen().df['job id'].isin(jobs)].reset_index()
    tags_df = pd.DataFrame.from_dict(alt['tags'].tolist())
    # Only Display Specific tags from dash_config
    tags_df = tags_df[['exp_name','exp_component']]
    # Dataframe of jobs
    #logger.debug(alt)
    # Dataframe of Tags of jobs
    #logger.debug(tags_df)
    alt = pd.merge(alt, tags_df, left_index=True, right_index=True)
    #alt.drop('tags',axis=1)
    # Now Calculate comparable jobs
    recs = alt.to_dict('records')
    cdict = {}
    for rec in recs:
        if (rec['exp_name'],rec['exp_component']) in cdict:
            cdict[(rec['exp_name'],rec['exp_component'])].update({rec['job id']})
        else:
            cdict[(rec['exp_name'],rec['exp_component'])] = {str(rec['job id'])}
    # Reconfigure output format with out
    out = [ ((exp_name,exp_component),cdict[(exp_name,exp_component)]) for exp_name, exp_component in cdict]
    logger.debug(out)
    return out

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


# Returns a list of model data to be converted into a dataframe
def _old_make_refs(x, name='', jobs=None, tags={}):
    from random import randint, getrandbits
    from .jobs import job_gen
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

def create_refmodel(jobs=None, name=None, tag=None):
    get_ref = {'tags': tag if tag else {},
                'updated_at': None,
                'created_at': datetime.datetime(2019, 11, 26, 22, 53, 42, 447548),
                'info_dict': None,
                'id': 1,
                'name': "Sample Model" + str(name)  if name else "Sample Ref Model",
                'op_tags': [],
                'enabled': True,
                'jobs': jobs if jobs else ['685000', '685003', '685016'],
                'modified_z_score': {'duration': [1.6944, 6615525773.0, 155282456.0],
                                    'num_procs': [3.0253, 3480.0, 68.0],
                                    'cpu_time': [10.8055, 113135329.0, 19597296.0]}}
    return get_ref
