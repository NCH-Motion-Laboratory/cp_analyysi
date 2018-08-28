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
import shutil


# some global parameters
rootdir = r'K:\CP_projekti_kopio'
plotdir = r'Z:\CP_projekti_analyysit\Normal_vs_cognitive'

# subject name globs
subj_globs_ = ['TD*', 'HP*', 'DP*']

# globs for each trial type
globs = dict()
globs['cognitive'] = ['*C?_*', '*K?_*']  # globs for cognitive trials
globs['normal'] = ['*N?_*']  # globs for normal
globs['tray'] = ['*T?_*']  # globs for tray trials

# exclude patterns - filenames including one of these will be dropped
files_exclude = ['stance', 'one', 'foam', 'hop', 'stand', 'balance',
                 'toes', 'toget', 'loitonnus', 'abduction']

logger = logging.getLogger(__name__)


def get_timestr():
    """ Get a second-resolution timestr (current time) that can be put into
    file names etc. """
    return strftime("%Y_%m_%d-%H%M%S", localtime())


def get_subjects():
    """ Get list of all subject names, e.g. 'TD01' """
    subjects = list()
    for glob_ in subj_globs_:
        glob_full = op.join(rootdir, glob_)
        subjects.extend(glob.glob(glob_full))
    # strip paths for get_files()
    subjects = [op.split(subj)[-1] for subj in subjects]
    # randomize order for debug purposes
    shuffle(subjects)
    return subjects


def make_clinical_copy(subject, destroot):
    """Make a copy of session with relevant trials only under destroot dir"""
    subjdir = op.join(rootdir, subject)
    if not op.isdir(subjdir):
        raise ValueError('Subject dir %s not found' % subjdir)

    datadirs = [dirn for dirn in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, dirn))]

    if not datadirs:
        raise ValueError('Subject dir %s does not contain any sessions'
                         % subjdir)

    if len(datadirs) > 1:
        raise ValueError('Subject dir %s contains multiple sessions'
                         % subjdir)
    datadir = datadirs[0]
    globs_ = globs['normal']

    # add other session files
    globs_.append('*Session.enf')
    globs_.append('*mp')
    globs_.append('*mkr')
    globs_.append('*sup')
    globs_.append('*vsk')

    files = list()
    for glob_ in globs_:
        glob_full = op.join(subjdir, datadir, glob_)
        files.extend(glob.glob(glob_full))

    # copy all files into new session dir
    subjdir_new = op.join(destroot, subject)
    if not op.isdir(subjdir_new):
        os.mkdir(subjdir_new)
    datadir_new = op.join(subjdir_new, datadir)
    if not op.isdir(datadir_new):
        os.mkdir(datadir_new)
    for f in files:
        shutil.copy2(f, datadir_new)

    # copy patient .enf into patient dir
    glob_full = op.join(subjdir, datadir, '*Patient.enf')
    patient_enf = glob.glob(glob_full)
    for f in patient_enf:
        shutil.copy2(f, subjdir_new)


def get_files(subject, types, ext='.c3d'):
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
    subjdir = op.join(rootdir, subject)
    if not op.isdir(subjdir):
        logger.warning('Subject directory not found: %s' % subjdir)
        return []

    datadirs = [file for file in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, file))]

    for datadir in datadirs:

        logger.debug('trying data dir %s/%s' % (subject, datadir))
        files = list()
        for glob_ in globs_:
            glob_ += ext
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
                     % (subject, '/'.join(types), len(files)))
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
