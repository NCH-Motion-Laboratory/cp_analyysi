# -*- coding: utf-8 -*-
"""
Autoprocess all CP subjects

@author: Jussi (jnu@iki.fi)
"""

import logging
import os.path as op
from time import localtime, strftime
import glob

import gaitutils
from gaitutils.nexus_scripts.nexus_autoprocess_session import autoproc_session
from gaitutils import cfg
from cp_common import get_files, rootdir

# name files according to script start time
timestr_ = strftime("%Y_%m_%d-%H%M%S", localtime())
# logfile - None for stdout logging
logfile = 'z:/CP_projekti_analyysit/cp_autoprocess_log_%s.txt' % timestr_

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# use the special config for CP project
cfg_file = 'c:/Users/Vicon123/.gaitutils_cp_projekti.cfg'
cfg.read(cfg_file)

# find all subjects
globs_ = ['TD*', 'HP*', 'DP*']
subjects = list()
for glob_ in globs_:
    glob_full = op.join(rootdir, glob_)
    subjects.extend(glob.glob(glob_full))

# strip paths for get_files()
subjects = [op.split(subj)[-1] for subj in subjects]

vi = gaitutils.nexus.viconnexus()

# run autoproc for each subject
for subject in subjects:
    # need to open trial to get Nexus to switch sessions
    c3ds = get_files(subject, 'normal')
    if not c3ds:
        logging.warning('no files for %s, skipping' % subject)
        continue
    c3d = op.splitext(c3ds[0])[0]
    vi.OpenTrial(c3d, 60)
    try:
        autoproc_session()
    except gaitutils.GaitDataError:
        logging.warning('autoproc error for %s, skipping' % subject)
        continue
