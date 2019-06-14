# -*- coding: utf-8 -*-
"""
Autoprocess all CP subjects

@author: Jussi (jnu@iki.fi)
"""

import subprocess
import time
import logging
import os.path as op

import gaitutils
from gaitutils.autoprocess import _do_autoproc
from gaitutils import cfg, nexus
from cp_common import get_files, get_subjects, get_timestr, logdir


def _start_nexus():
    """Start Vicon Nexus"""
    logging.debug('starting Nexus')
    
    exe = op.join(nexus._find_nexus_path(), 'Nexus.exe')
    p = subprocess.Popen([exe])
    time.sleep(10)
    return p


def _kill_nexus(p):
    """Kill Vicon Nexus process p"""
    logging.debug('terminating Nexus')
    p.terminate()
    time.sleep(5)


# trial types to process
trial_types = ['normal', 'cognitive']

# logfile - None for stdout logging
logfilename = 'cp_autoprocess_log_%s.txt' % get_timestr()
logfile = op.join(logdir, logfilename)

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# use the special config for CP project
#cfg_file = 'c:/Users/Vicon123/.gaitutils_cp_projekti.cfg'
#cfg.read(cfg_file)

subjects = get_subjects()
subjects = ['TD3']

logging.debug('start global autoproc for %d subjects:' % len(subjects))
logging.debug('%s' % subjects)

# run autoproc for each subject
for subject in subjects:
    #p = _start_nexus()
    vi = gaitutils.nexus.viconnexus()
    # look for x1d instead of c3d (c3d files may not exist yet)
    trials_ = get_files(subject, 'normal', ext='.x1d')
    if not trials_:
        logging.warning('no files for %s, skipping' % subject)
        continue
    trial_ = op.splitext(trials_[0])[0]
    # need to open trial to get Nexus to switch sessions
    vi.OpenTrial(trial_, 60)
    try:
        enffiles = get_files(subject, trial_types, ext='.Trial.enf')
        _do_autoproc(enffiles)
    except gaitutils.GaitDataError:
        logging.warning('autoproc error for %s, skipping' % subject)
    #_kill_nexus(p)

logging.debug('global autoproc finished')
print 'done'
