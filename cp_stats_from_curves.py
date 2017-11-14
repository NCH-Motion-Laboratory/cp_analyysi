# -*- coding: utf-8 -*-
"""

plan:


CP-projektin analyysiskripti:
laske numeerista dataa kävelykäyristä

tilanteet:
    strike, toeoff, max, min, contact_max

muuttujat:

hip flexion:
    strike, toeoff

knee flexion:
    strike
    contact_max

ankle dorsi/plant:
    strike, toeoff
    contact_max

thorax lateral flex:
    max, min

thorax rotation:
    max, min


@author: Jussi (jnu@iki.fi)
"""


from __future__ import print_function
from openpyxl import Workbook
from collections import defaultdict
import matplotlib.pyplot as plt
import glob
import numpy as np
import sys
import os
import os.path as op
import scipy
import time
import logging

from cp_common import get_files, write_workbook
import gaitutils
from gaitutils import cfg

logger = logging.getLogger(__name__)

# the vars of interest
stats_vars = ['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX',
              'ThoraxAnglesY', 'ThoraxAnglesZ']

# which values to extract for each variable - set undesired ones to False
extract = {key: defaultdict(lambda: True) for key in stats_vars}
extract['HipAnglesX']['max'] = False
extract['HipAnglesX']['min'] = False
extract['HipAnglesX']['contact_max'] = False

extract['KneeAnglesX']['max'] = False
extract['KneeAnglesX']['min'] = False

extract['AnkleAnglesX']['min'] = False
extract['AnkleAnglesX']['max'] = False

extract['ThoraxAnglesY']['strike'] = False
extract['ThoraxAnglesY']['contact_max'] = False

extract['ThoraxAnglesZ']['strike'] = False
extract['ThoraxAnglesZ']['contact_max'] = False

# max. dist for detecting outlier curves
max_dist = 40


def _process_data(subject, cond):

    # get list of files and average
    files = get_files(subject, cond)
    avgdata, stddata, N_ok, _ = gaitutils.stats.average_trials(files,
                                                               max_dist=max_dist)

    logger.debug('averaging stats for %s / %s:' % (subject, cond))
    for varname_ in stats_vars:
        for side in ['R', 'L']:
            varname = side + varname_
            logger.debug('%s: %d averages' % (varname, N_ok[varname]))

    # these are common for all vars
    range_ = ''
    type_ = 1
    unit_ = 'deg'

    for varname_ in stats_vars:
        for side in ['R', 'L']:
            varname = side + varname_
            data = avgdata
            context = 'right' if side == 'R' else 'left'
            # value at foot strike
            extr = extract[varname_]
            if extr['strike']:
                yield ['%s at foot strike, %s %s' % (varname_, context, cond),
                       unit_, range_, type_, data[varname][0]]
            # maximum over cycle
            if extr['max']:
                yield ['%s maximum, %s %s' % (varname_, context, cond),
                       unit_, range_, type_, data[varname].max()]
            # minimum over cycle
            if extr['min']:
                yield ['%s minimum, %s %s' % (varname_, context, cond),
                       unit_, range_, type_, data[varname].min()]
            # maximum during contact phase
            if extr['contact_max']:
                xind = scipy.signal.argrelextrema(data[varname], np.greater)[0]
                xind_contact = xind[np.where(xind < 60)]
                cpm = (data[varname][xind_contact].max() if
                       len(xind_contact) > 0 else '')
                yield ['%s max. during contact phase, %s %s'
                       % (varname_, context, cond), unit_, range_, type_, cpm]


def get_results(subjects):

    results = dict()
    for j, subject in enumerate(subjects):
        for cond in ['normal', 'cognitive']:
            for r in _process_data(subject, cond):
                var = r[0]
                if var not in results:
                    results[var] = r
                else:
                    results[var].append(r[-1])
    logger.debug('finished')
    return results











