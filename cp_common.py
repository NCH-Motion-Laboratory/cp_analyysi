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
globs['cognitive'] = ['*C?_*.c3d', '*K?_*.c3d']  # globs for cognitive
globs['normal'] = ['*N?_*.c3d']  # globs for normal

# exclude patterns - filenames including one of these will be dropped
files_exclude = ['stance', 'one', 'foam', 'hop']

logger = logging.getLogger(__name__)


def get_files(subject, type):
    """Get trial files according to given subject and trial type"""
   
    if type not in globs:
        raise Exception('Invalid trial type')
    else:
        globs_ = globs[type]

    logger.debug('finding trial files for %s' % subject)
    # try to auto find data dirs under subject dir
    subjdir = op.join(rootdir, subject)
    if not op.isdir(subjdir):
        logger.warning('Subject directory not found: %s' % subjdir)
        return []

    datadirs = [file for file in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, file))]

    for datadir in datadirs:

        logger.debug('trying data dir %s' % datadir)
        files = list()
        for glob_ in globs_:
            glob_full = op.join(subjdir, datadir, glob_)
            files.extend(glob.glob(glob_full))

        files_exc = [it for it in files if any([exc.lower() in it.lower()
                     for exc in files_exclude])]

        files = list(set(files) - set(files_exc))

        # does it look like a proper datadir?
        if len(files) < 10:
            logger.debug('%s is probably not a CP data dir' % datadir)
            continue

        logger.debug('subject %s, %s trials: found %d files:'
                     % (subject, type, len(files)))
        for fn in files:
            logger.debug(fn)
        if files_exc:
            logger.debug('excluded files:')
            for fn in files_exc:
                logger.debug(fn)
        return files

    logger.warning('no files found for %s' % subject)
    return []


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
