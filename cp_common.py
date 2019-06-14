# -*- coding: utf-8 -*-
"""

shared defs for CP project

@author: Jussi (jnu@iki.fi)
"""


from __future__ import print_function
from random import shuffle
import glob
import os
import os.path as op
from openpyxl import Workbook
from time import localtime, strftime
import logging
import json

logger = logging.getLogger(__name__)


# read cp_analysis.json from home dir
homedir = op.expanduser('~')
cfg_json = op.join(homedir, 'cp_analysis.json')
if not op.isfile(cfg_json):
    raise ValueError('must create config file %s' % cfg_json)
with open(cfg_json, 'rb') as f:
    params = json.load(f)

if not op.isdir(params['rootdir']):
    raise ValueError('configured root dir %s does not exist')

# globs for each trial type
globs = dict()
globs['cognitive'] = ['*C?_*', '*K?_*']  # globs for cognitive trials
globs['normal'] = ['*N?_*']  # globs for normal
globs['tray'] = ['*T?_*']  # globs for tray trials

# exclude patterns - filenames including one of these will be dropped
files_exclude = ['stance', 'one', 'foam', 'hop', 'stand', 'balance',
                 'toes', 'toget', 'loitonnus', 'abduction']


def _glob_all(globs, prefix=None, postfix=None):
    """Glob from a list, adding prefix (maybe a directory)"""
    if not isinstance(globs, list):
        globs = [globs]
    files = list()
    for g in globs:
        glob_ = op.join(prefix, g) if prefix else g
        glob_ += postfix if postfix is not None else ''
        files.extend(glob.glob(glob_))
    return files


def get_timestr():
    """ Get a second-resolution timestr (current time) that can be put into
    file names etc. """
    return strftime("%Y_%m_%d-%H%M%S", localtime())


def get_subjects():
    """ Get list of all subject names, e.g. 'TD01' """
    subjects = list()
    for glob_ in params['subj_globs_']:
        glob_full = op.join(params['rootdir'], glob_)
        subjects.extend(glob.glob(glob_full))
    # strip paths for get_files()
    subjects = [op.split(subj)[-1] for subj in subjects]
    # randomize order for debug purposes
    shuffle(subjects)
    return subjects


def get_files(subject, types, ext='c3d'):
    """ Get trial files according to given subject and trial type
    (e.g. 'normal') and file extension """

    if not isinstance(types, list):
        types = [types]

    globs_ = list()

    for t in types:
        if t not in globs:
            raise Exception('Invalid trial type')
        else:
            globs_ += globs[t]

    logger.debug('finding trial files for %s' % subject)
    # try to auto find data dirs under subject dir
    subjdir = op.join(params['rootdir'], subject)
    if not op.isdir(subjdir):
        logger.warning('Subject directory not found: %s' % subjdir)
        return list()

    datadirs = [file for file in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, file))]

    for datadir in datadirs:

        logger.debug('trying data dir %s/%s' % (subject, datadir))
        prefix = op.join(subjdir, datadir)
        files = _glob_all(globs_, prefix=prefix, postfix=ext)

        files_exc = [it for it in files if any([exc.lower() in it.lower()
                     for exc in files_exclude])]
        files = list(set(files) - set(files_exc))
        logger.debug('excluding: %s' % files_exc)

        if len(files) < 10:
            logger.debug('%s is probably not a CP data dir' % datadir)
            continue

        logger.debug('subject %s, %s trials: found %d files:'
                     % (subject, '/'.join(types), len(files)))

        return files

    logger.warning('no files found for %s' % subject)
    return list()


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
