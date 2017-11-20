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

import logging


import cp_stats_from_curves
import cp_walk_parameters
from cp_common import write_workbook, get_subjects, get_timestr


subjects = get_subjects()

timestr_ = get_timestr()
# logfile - None for stdout logging
logfile = 'z:/CP_projekti_analyysit/cp_analysis_log_%s.txt' % timestr_
# output file
xls_filename = 'z:/CP_projekti_analyysit/cp_analysis_%s.xlsx' % timestr_

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(funcName)s: %(message)s')

# exclude some loggers to reduce noise
logging.getLogger('gaitutils.trial').setLevel(logging.WARNING)
logging.getLogger('gaitutils.utils').setLevel(logging.WARNING)
logging.getLogger('gaitutils.emg').setLevel(logging.WARNING)
logging.getLogger('gaitutils.eclipse').setLevel(logging.WARNING)
logging.getLogger('gaitutils.c3d').setLevel(logging.WARNING)
logging.getLogger('gaitutils.stats').setLevel(logging.WARNING)

results_all = dict()
results_all.update(cp_stats_from_curves.get_results(subjects))
results_all.update(cp_walk_parameters.get_results(subjects))

write_workbook([['']*4 + subjects] + sorted(results_all.values()),
               xls_filename)


