# -*- coding: utf-8 -*-
"""
Autoprocess all CP subjects

@author: Jussi (jnu@iki.fi)
"""

import logging
import os.path as op
from time import localtime, strftime

import gaitutils
from gaitutils.nexus_scripts.nexus_autoprocess_session import autoproc_session
from gaitutils import cfg
from cp_common import get_files, get_subjects

# name files according to script start time
timestr_ = strftime("%Y_%m_%d-%H%M%S", localtime())
# logfile - None for stdout logging
logfile = 'z:/CP_projekti_analyysit/cp_autoprocess_log_%s.txt' % timestr_

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# use the special config for CP project
cfg_file = 'c:/Users/Vicon123/.gaitutils_cp_projekti.cfg'
cfg.read(cfg_file)

subjects = get_subjects()

vi = gaitutils.nexus.viconnexus()

logging.debug('start global autoproc for %d subjects:' % len(subjects))
logging.debug('%s' % subjects)

# run autoproc for each subject
for subject in subjects:
    # look for x1d instead of c3d (c3d files may not exist yet)
    c3ds = get_files(subject, 'normal', ext='.x1d')
    if not c3ds:
        logging.warning('no files for %s, skipping' % subject)
        continue
    c3d = op.splitext(c3ds[0])[0]
    # need to open trial to get Nexus to switch sessions
    vi.OpenTrial(c3d, 60)
    try:
        autoproc_session()
    except gaitutils.GaitDataError:
        logging.warning('autoproc error for %s, skipping' % subject)
        continue

logging.debug('global autoproc finished')
print 'done'
