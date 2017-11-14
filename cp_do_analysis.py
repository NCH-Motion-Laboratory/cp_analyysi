# -*- coding: utf-8 -*-
"""
idea:

-each file has get_results() function that takes subjects as arg and returns
dict keyed as variable: data, where data is a list of headers + values for each
subject

-merge dicts to get all results, write to xlsx

-need to capture logs also


@author: Jussi (jnu@iki.fi)
"""

import logging

import cp_stats_from_curves
import cp_walk_parameters
from cp_common import write_workbook

# subjects to analyze
subjects = ['TD26', 'TD24', 'TD25', 'TD23']
subjects = ['TD26', 'TD24']
# logfile - None for stdout logging
logfile = 'c:/Temp/cp_log.txt'
# output file
xls_filename = 'c:/Temp/foobar1.xlsx'

logging.basicConfig(filename=logfile, level=logging.DEBUG,
                    format='%(asctime)s %(module)s:%(message)s')


# get results
results_all = dict()
results_all.update(cp_stats_from_curves.get_results(subjects))
results_all.update(cp_walk_parameters.get_results(subjects))

write_workbook([['']*4 + subjects] + sorted(results_all.values()),
               xls_filename)









