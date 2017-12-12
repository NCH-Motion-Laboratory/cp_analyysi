# -*- coding: utf-8 -*-
"""
Autoprocess all CP subjects

Nexus hangs cause problems - maybe try moving files to local disk?

@author: Jussi (jnu@iki.fi)
"""

import subprocess
import time
import logging
import os.path as op
import os

import gaitutils
from gaitutils.nexus_scripts.nexus_autoprocess_session import autoproc_session
from gaitutils import cfg, nexus
from cp_common import get_files, get_subjects, get_timestr


def _start_nexus():
    """Start Vicon Nexus"""
    logging.debug('starting Nexus')
    exe = op.join(cfg.general.nexus_path, 'Nexus.exe')
    p = subprocess.Popen([exe])
    time.sleep(10)
    return p


def _kill_nexus(p):
    """Kill Vicon Nexus process p"""
    logging.debug('terminating Nexus')
    p.terminate()
    time.sleep(5)


# logfile - None for stdout logging
logfile = 'z:/CP_projekti_analyysit/cp_autoprocess_log_%s.txt' % get_timestr()

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# use the special config for CP project
cfg_file = 'c:/Users/Vicon123/.gaitutils_cp_projekti.cfg'
cfg.read(cfg_file)

# process subjects that were not already processed
subjects_done = ['TD04']
subjects_all = get_subjects()
subjects = list(set(subjects_all) - set(subjects_done))

# or specify a list
subjects = ['TD07', 'HP10', 'HP09']

logging.debug('start global autoproc for %d subjects:' % len(subjects))
logging.debug('%s' % subjects)

# run autoproc for each subject
for subject in subjects:
    p = _start_nexus()
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
        autoproc_session()
    except gaitutils.GaitDataError:
        logging.warning('autoproc error for %s, skipping' % subject)
        _kill_nexus(p)
        continue
    _kill_nexus(p)

logging.debug('global autoproc finished')
print 'done'
