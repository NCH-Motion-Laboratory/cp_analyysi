# -*- coding: utf-8 -*-
"""
CP, check autoproc results

Load random trials sequentially in Nexus. Show kinematics. Save evaluation to
xls

@author: Jussi (jnu@iki.fi)
"""

import sys
import os.path as op
from random import shuffle

import gaitutils
from gaitutils import GaitDataError

from cp_common import write_workbook, get_subjects, get_timestr, get_files


N = 100
trial_types = ['normal', 'cognitive']

timestr_ = get_timestr()
# results shall be entered into this workbook
xls_filename = 'K:/CP_projekti_analyysit/cp_autoproc_check_%s.xlsx' % timestr_

trials = list()
subjects = get_subjects()

for subj in subjects:
    trials += get_files(subj, trial_types)
shuffle(trials)
print 'Got trials'

trials_ = trials[:N]
write_workbook([trials_], xls_filename)

vicon = gaitutils.nexus.viconnexus()

evs = list()
for trial in trials_:
    trialbase = op.splitext(trial)[0]
    print 'Opening %s' % trial
    vicon.OpenTrial(trialbase, 200)
    print 'Plotting kinematics, close window after review...'
    sys.stdout.flush()
    try:
        gaitutils.nexus_kinallplot.do_plot()
    except (GaitDataError, ValueError):
        print 'Failed to plot kinematics'
    enf = '%s.Trial.enf' % trialbase
    desc = gaitutils.eclipse.get_eclipse_keys(enf)['DESCRIPTION']
    print 'Description: %s' % desc
    print 'Enter evaluation (hit Enter for ok):'
    sys.stdout.flush()
    ev = raw_input()
    if not ev:
        ev = 'ok'
    evs.append(ev)

write_workbook([trials_, evs], xls_filename)
