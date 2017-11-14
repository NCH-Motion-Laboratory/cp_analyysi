# -*- coding: utf-8 -*-
"""

shared defs for CP project

@author: Jussi (jnu@iki.fi)
"""


from __future__ import print_function
import glob
import os
import os.path as op
from openpyxl import Workbook
import logging

# some global parameters
rootdir = 'Z:\\Userdata_Vicon_Server\\CP-projekti'
plotdir = "Z:\\CP_projekti_analyysit\\Normal_vs_cognitive"

# globs for each trial type
globs = dict()
globs['cognitive'] = '*_C?_*.c3d'  # glob for cognitive
globs['normal'] = '*_N?_*.c3d'  # glob for normal

logger = logging.getLogger(__name__)


def get_files(subject, type):
    """Get trial files according to given subject and trial type"""
    if type not in globs:
        raise Exception('Invalid trial type')
    else:
        glob_ = globs[type]

    # try to auto find data dirs under subject dir
    subjdir = op.join(rootdir, subject)
    datadirs = [file for file in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, file))]
    if len(datadirs) > 1:
        raise Exception('Multiple data dirs under subject')
    datadir = datadirs[0]

    files = list()
    glob_full = op.join(subjdir, datadir, glob_)
    files += glob.glob(glob_full)

    if not files:
        raise Exception('No trials for subject %s and glob %s' %
                        (subject, glob_))
    logger.debug('subject %s, %s trials: found %d files:'
                 % (subject, type, len(files)))
    for fn in files:
        logger.debug(fn)
    return files


def write_workbook(results, filename, first_col=1, first_row=1):
    """Write results into .xlsx file (filename). results must be a list of
    lists which represent the columns to write. first_col and first_row
    specify the column and row where to start writing (1-based) """
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Gait analysis parameters"
    for j, col in enumerate(results):
        for k, val in enumerate(col):
            ws1.cell(column=j+1+first_col, row=k+1+first_row, value=val)
    logger.debug('saving %s' % filename)
    wb.save(filename=filename)
