"""Mock epmt_query methods
"""

import datetime
from datetime import timedelta
from random import choice
from copy import deepcopy
from logging import getLogger
import pandas as pd
from jobs import JobGen

# We log how we want
# pylint: disable=invalid-name, logging-format-interpolation

logger = getLogger(__name__)

# Due to this being a mock file there will be unused arguments & dangerous defaults
# pylint: disable=unused-argument,dangerous-default-value

# Due to sample job dictionary lines will be long
# pylint: disable=line-too-long

SAMPLE_JOB = {'duration': 6460243317.0,
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


class Models:
    """Models
    model class to hold list of models and increment an id
    """
    id = 0
    model_list = []


def create_refmodel(name, jobs=[], tag={}, enabled=True):
    """ This mock reference model method accepts a job name
    jobs and tag.
    Appends to the model list a new model & increments the model.id
    Returns:
    The newly created model dictionary
    """
    Models.id = Models.id + 1
    Models.model_list.append({'id': Models.id, 'name': name, 'created_at': datetime.date.today(),
                              'tags': tag, 'jobs': jobs, 'enabled': enabled})
    Models.id = Models.id + 1
    return {'id': Models.id, 'name': name, 'created_at': datetime.date.today(),
            'tags': tag, 'jobs': jobs, 'enabled': enabled}


def get_refmodels():
    """ Returns a list of models
    """
    return Models.model_list


def delete_refmodels(*ref_ids):
    """ Incomplete, Should remove a reference model via the id
    """
    if not ref_ids:
        logger.warning(
            "You must specify one or more reference model IDs to delete")
        return 0
    return ''


def get_jobs(jobs=None, tags=None, fltr=None, order=None, limit=None, offset=0, when=None,
             before=None, after=None, hosts=[],
             fmt='dict', annotations=None, analyses=None, merge_proc_sums=True,
             exact_tag_only=False):
    """ Use SAMPLE_JOB real job as template
     replace jobid with new number
     return list of limit of jobs
     def get_jobs(limit=None, fmt='df', offset=0):
     if offset >= limit: offset = limit
    """
    if offset > 0:
        # This isn't quite right..
        # df[offset:offset+limit]
        limit = offset + limit
    logger.info("Getting jobs...Limit{} Offset{}".format(limit, offset))
    sample_component = '_annual_rho2_1x1deg'
    component_list = ['ocean', 'land', 'mountian']
    sample_name = '_historical'
    name_list = ['ESM0', 'ESM1']
    result = []
    for njob in range(limit):
        job = dict(SAMPLE_JOB)
        job['jobid'] = str(1234000 + njob)
        job['Processed'] = 1
        job['start'] = job['start'] + timedelta(days=njob)
        job['end'] = job['end'] + timedelta(days=njob)
        name = name_list[njob % 2]
        job['tags']['exp_name'] = name + sample_name
        if job['jobid'] == str(1234002):
            job['tags']['exp_name'] = "mismatch_test"
        comp = component_list[njob % 3] + sample_component
        job['tags']['exp_component'] = str(comp)
        result.append(deepcopy(job))
    return result[offset:]


def comparable_job_partitions(jobs, matching_keys=['exp_name', 'exp_component']):
    """Mock comparable_jobs
    Accepts jobid's, identifies based on matching_keys which are compatible
    Returns [ (('matchname','matchcomponent'), {set of matchjobids}), ...]
    """

    # Typically jobids are only passed
    # I need to get the jobids name and component
    alt = JobGen().jobs_df[JobGen().jobs_df['job id'].isin(jobs)].reset_index()
    tags_df = pd.DataFrame.from_dict(alt['tags'].tolist())
    # Only Display Specific tags from dash_config
    tags_df = tags_df[['exp_name', 'exp_component']]
    # Dataframe of jobs
    # logger.debug(alt)
    # Dataframe of Tags of jobs
    # logger.debug(tags_df)
    alt = pd.merge(alt, tags_df, left_index=True, right_index=True)
    # alt.drop('tags',axis=1)
    # Now Calculate comparable jobs
    recs = alt.to_dict('records')
    cdict = {}
    for rec in recs:
        if (rec['exp_name'], rec['exp_component']) in cdict:
            cdict[(rec['exp_name'], rec['exp_component'])
                  ].update({rec['job id']})
        else:
            cdict[(rec['exp_name'], rec['exp_component'])] = {
                str(rec['job id'])}
    # Reconfigure output format with out
    out = [((exp_name, exp_component), cdict[(exp_name, exp_component)])
           for exp_name, exp_component in cdict]
    logger.debug(out)
    return out


def get_procs(
        jobs=[],
        tags=None, fltr=None, order=None, limit=None, when=None, hosts=[],
        fmt='dict', merge_threads_sums=True, exact_tag_only=False):
    '''
    Implemented:
    jobs: list or string/int
    limit: int
    jobid,exename and path

    jobid matches request
    exename randomized
    path matches randomized exename
    '''
    result = []

    if (limit is None) and (fmt != 'orm'):
        limit = 10000
        logger.info('No limit set, defaults to {0}. Set limit to 0 to avoid limits'.format(limit))
    exelist = [
        "bash", "bsd-csh", "bunzip2", "busybox", "bzcat", "bzcmp", "bzdiff", "bzegrep", "bzexe",
        "bzfgrep", "bzgrep", "bzip2", "bzip2recover", "bzless", "bzmore", "cat", "chacl", "chgrp",
        "chmod", "chown", "chvt", "cp", "cpio", "csh", "dash", "date", "dd", "df", "dir", "dmesg",
        "dnsdomainname", "domainname", "dumpkeys", "echo", "ed", "efibootmgr", "egrep", "false",
        "fgconsole", "fgrep", "findmnt", "fuser", "fusermount", "getfacl", "grep", "gunzip",
        "gzexe", "gzip", "hciconfig", "hostname", "ip", "journalctl", "kbd_mode", "keyctl", "kill",
        "kmod", "less", "lessecho", "lessfile", "lesskey", "lesspipe", "ln", "loadkeys", "login",
        "loginctl", "lowntfs-3g", "ls", "lsblk", "lsmod", "mkdir", "mknod", "mktemp", "more",
        "mount", "mountpoint", "mt", "mt-gnu", "mv", "nano", "nc", "nc.openbsd", "netcat",
        "netstat", "networkctl", "nisdomainname", "ntfs-3g", "ntfs-3g.probe", "ntfs-3g.secaudit",
        "ntfs-3g.usermap", "ntfscat", "ntfscluster", "ntfscmp", "ntfsfallocate", "ntfsfix",
        "ntfsinfo", "ntfsls", "ntfsmove", "ntfstruncate", "ntfswipe", "open", "openvt", "pidof",
        "ping", "ping6", "plymouth", "ps", "pwd", "rbash", "readlink", "red", "rm", "rmdir",
        "rnano", "run-parts", "sed", "setfacl", "setfont", "setupcon", "sh", "sh.distrib", "sleep",
        "ss", "static-sh", "stty", "su", "sync", "systemctl", "systemd", "systemd-ask-password",
        "systemd-escape", "systemd-hwdb", "systemd-inhibit", "systemd-machine-id-setup",
        "systemd-notify", "systemd-tmpfiles", "systemd-tty-ask-password-agent", "tailf", "tar",
        "tcsh", "tempfile", "touch", "true", "udevadm", "ulockmgr_server", "umount", "uname",
        "uncompress", "unicode_start", "vdir", "wdctl", "which", "whiptail", "ypdomainname", "zcat",
        "zcmp", "zdiff", "zegrep", "zfgrep", "zforce", "zgrep", "zless", "zmore", "znew"]

    sample_proc = {'id': 36416,
                   'start': datetime.datetime(2019, 6, 16, 13, 54, 28, 878022),
                   'end': datetime.datetime(2019, 6, 16, 14, 6, 18, 107548),
                   'duration': 709229526.0000001,
                   'created_at': datetime.datetime(2019, 12, 17, 21, 1, 32, 442541),
                   'updated_at': datetime.datetime(2019, 12, 17, 21, 1, 32, 442546),
                   'tags': {'op': 'dmput', 'op_instance': '2', 'op_sequence': '89'},
                   'job': jobs,
                   'host': 'pp028',
                   'user': 'Jeffrey.Durachta',
                   'group': None,
                   'numtids': 1,
                   'cpu_time': 733887.0,
                   'inclusive_cpu_time': 592078553.0,
                   'exename': 'tcsh',
                   'path': '/bin/tcsh',
                   'args': '-f /home/Jeffrey.Durachta/ESM4/DECK/ESM4_historical_D151/gfdl.ncrc4-intel16-prod-openmp/scripts/postProcess/ESM4_historical_D151_ocean_month_rho2_1x1deg_18890101.tags',
                   'pid': 1941,
                   'ppid': 1940,
                   'pgid': 1932,
                   'sid': 1927,
                   'gen': 0,
                   'exitcode': 0,
                   'parent': None,
                   'PERF_COUNT_SW_CPU_CLOCK': 679559948,
                   'cancelled_write_bytes': 4096,
                   'delayacct_blkio_time': 0,
                   'guest_time': 0,
                   'inblock': 8424,
                   'invol_ctxsw': 140,
                   'majflt': 10,
                   'minflt': 38676,
                   'outblock': 10648,
                   'processor': 0,
                   'rchar': 297337,
                   'rdtsc_duration': 2452426270720,
                   'read_bytes': 4313088,
                   'rssmax': 5512,
                   'syscr': 1327,
                   'syscw': 1313,
                   'systemtime': 311952,
                   'time_oncpu': 734283936,
                   'time_waiting': 414940469,
                   'timeslices': 4042,
                   'user+system': 733887,
                   'usertime': 421935,
                   'vol_ctxsw': 3901,
                   'wchar': 82957,
                   'write_bytes': 5451776,
                   'jobid': '692544'}
    for j in jobs if isinstance(jobs, list) else [jobs]:
        for n in range(limit):
            proc = sample_proc
            proc['jobid'] = j
            proc['exename'] = choice(exelist)
            proc['path'] = '/bin/'+proc['exename']
            result.append(deepcopy(proc))
    return result
