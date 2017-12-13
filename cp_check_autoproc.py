# -*- coding: utf-8 -*-
"""
CP, check autoproc results

Load random trials sequentially in Nexus

@author: Jussi (jnu@iki.fi)
"""

import os.path as op
from random import shuffle

import gaitutils

from cp_common import write_workbook, get_subjects, get_timestr, get_files


N = 100
trial_types = ['normal', 'cognitive']

timestr_ = get_timestr()
# results shall be entered into this workbook
xls_filename = 'z:/CP_projekti_analyysit/cp_autoproc_check_%s.xlsx' % timestr_

trials = list()
subjects = get_subjects()

for subj in subjects:
    trials += get_files(subj, trial_types)
shuffle(trials)

trials_ = trials[:N]
write_workbook([trials_], xls_filename)

vicon = gaitutils.nexus.viconnexus()

for trial in trials_:
    vicon.OpenTrial(op.splitext(trial)[0], 200)
    print 'Opened %s, press enter to open next trial'
