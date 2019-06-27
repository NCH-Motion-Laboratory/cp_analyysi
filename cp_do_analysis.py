# -*- coding: utf-8 -*-
"""
idea:

-each file has get_results() function that takes subjects as arg and returns
dict keyed as variable: data, where data is a list of headers + values for each
subject

-merge dicts to get all results, write to xlsx

-capture logs


@author: Jussi (jnu@iki.fi)
"""

import os.path as op
import logging

import cp_stats_from_curves
import cp_walk_parameters
from cp_common import write_workbook, get_subjects, get_timestr, params


# logfile - None for stdout logging
timestr_ = get_timestr()
logfilename = 'cp_analysis_log_%s.txt' % timestr_
logfile = op.join(params['logdir'], logfilename)
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')
xls_filename_ = 'cp_analysis_%s.xlsx' % timestr_
xls_filename = op.join(params['plotdir'], xls_filename_)
logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# exclude some loggers to reduce noise
logging.getLogger('gaitutils.trial').setLevel(logging.WARNING)
logging.getLogger('gaitutils.utils').setLevel(logging.WARNING)
logging.getLogger('gaitutils.emg').setLevel(logging.WARNING)
logging.getLogger('gaitutils.eclipse').setLevel(logging.WARNING)
logging.getLogger('gaitutils.c3d').setLevel(logging.WARNING)
logging.getLogger('gaitutils.stats').setLevel(logging.WARNING)

subjects = params['analysis_subjects']
if not subjects:
    subjects = get_subjects()

results_all = dict()
results_curves = cp_stats_from_curves.get_results(subjects)
results_params = cp_walk_parameters.get_results(subjects)

results_all.update(results_curves)
results_all.update(results_params)

write_workbook([['']*4 + subjects] + sorted(results_all.values()),
               xls_filename)
