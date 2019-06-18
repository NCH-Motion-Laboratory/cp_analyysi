# -*- coding: utf-8 -*-
"""
Autoprocess CP subjects

@author: Jussi (jnu@iki.fi)
"""

import subprocess
import time
import logging
import os.path as op

import gaitutils
from gaitutils.autoprocess import _do_autoproc
from gaitutils import cfg, nexus, configdot
from cp_common import get_files, get_subjects, get_timestr, homedir, params

logger = logging.getLogger(__name__)


def _start_nexus():
    """Start Vicon Nexus"""
    logger.debug('starting Nexus')
    
    exe = op.join(nexus._find_nexus_path(), 'Nexus.exe')
    p = subprocess.Popen([exe])
    time.sleep(10)
    return p


def _kill_nexus(p):
    """Kill Vicon Nexus process p"""
    logger.debug('terminating Nexus')
    p.terminate()
    time.sleep(5)


# logfile - None for stdout logging
logfilename = 'cp_autoprocess_log_%s.txt' % get_timestr()
logfile = op.join(params['logdir'], logfilename)
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# use the special config for CP project
cfg_file = params['autoproc_config']
cfg_cp = configdot.parse_config(cfg_file)
configdot.update_config(cfg, cfg_cp)

if not params['autoproc_subjects']:
    autoproc_subjects = get_subjects()
else:
    autoproc_subjects = params['autoproc_subjects']

logger.debug('start global autoproc for %d subjects:' % len(autoproc_subjects))
logger.debug('%s' % autoproc_subjects)

# run autoproc for each subject
for subject in autoproc_subjects:
    p = _start_nexus()
    vi = gaitutils.nexus.viconnexus()
    # look for x1d instead of c3d (c3d files may not exist yet)
    trials_ = get_files(subject, 'normal', ext='.x1d')
    if not trials_:
        logger.warning('no files for %s, skipping' % subject)
        continue
    trial_ = op.splitext(trials_[0])[0]
    # need to open trial to get Nexus to switch sessions
    vi.OpenTrial(trial_, 60)
    try:
        enffiles = get_files(subject, params['autoproc_types'], ext='.Trial.enf')
        _do_autoproc(enffiles, pipelines_in_proc=False)
    except gaitutils.GaitDataError:
        logger.warning('autoproc error for %s, skipping' % subject)
    _kill_nexus(p)

logger.debug('global autoproc finished')
print 'done'
