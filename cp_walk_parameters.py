# -*- coding: utf-8 -*-
"""
CP project:
read time / distance vars from c3d files

@author: Jussi (jnu@iki.fi)
"""

from __future__ import print_function
import numpy as np
import logging

from gaitutils import analysis
from cp_common import get_files


logger = logging.getLogger(__name__)

# analysis vars of interest
vars = ['Stride Time',
        'Opposite Foot Off',
        'Double Support',
        'Opposite Foot Contact',
        'Single Support',
        'Step Length',
        'Foot Off',
        'Walking Speed',
        'Stride Length',
        'Step Time',
        'Cadence']


def _read_data(subject, vars, cond):
    """ Returns a dict of parameters for each trial """
    Cfiles = get_files(subject, cond)
    # 'unknown' is the default condition name
    datas = {f: c3d.get_analysis(f)['unknown'] for f in Cfiles}
    datas_ok = {f: data for f, data in datas.items()
                if all([var in data for var in vars])}
    logger.debug('%s/%s: %d files read, %d files contained data' %
                 (subject, cond, len(datas), len(datas_ok)))
    not_ok = set(datas.keys()) - set(datas_ok.keys())
    if not_ok:
        logger.debug('following files not ok:')
        for fn in not_ok:
            logger.debug(fn)
    if datas_ok:
        logger.debug('including files:')
        for fn in datas_ok:
            logger.debug(fn)
    return datas_ok


def _process_data(datas, vars, cond):
    """Yields lists for each variable"""

    if not datas:
        logger.debug('no data, terminating')
        raise ValueError('No data')

    # for picking units
    data0 = datas.values()[0]

    # collect into dict
    results = dict()
    for var in vars:
        results[var] = dict()
        results[var]['unit'] = data0[var]['unit']
        for context in ['Right', 'Left']:
            results[var][context] = list()
            for f, data in datas.items():
                if context not in data[var]:
                    logger.debug('missing data for %s: %s in file %s' %
                                 (var, context, f))
                else:
                    thisdata = data[var][context]
                    if thisdata is not None:
                        results[var][context].append(thisdata)
                    else:
                        logger.debug('data is None for %s: %s in file %s' %
                                     (var, context, f))
    # these are common to all vars
    range_ = ''
    type_ = 1
    for var in vars:
        unit_ = results[var]['unit']
        for context in ['Right', 'Left']:
            data = np.array(results[var][context])
            mean_ = data.mean()
            std_ = data.std()
            yield ['%s mean, %s %s' % (var, context.lower(), cond),
                   unit_, range_, type_, mean_]
            yield ['%s stddev, %s %s' % (var, context.lower(), cond),
                   unit_, range_, type_, std_]


def get_results(subjects):
    if not isinstance(subjects, list):
        subjects = [subjects]
    logger.debug('starting time-distance analysis')
    results = dict()
    for j, subject in enumerate(subjects):
        logger.debug('processing subject %s' % subject)
        for cond in ['normal']:
            datas = _read_data(subject, vars, cond)
            for r in _process_data(datas, vars, cond):
                var = r[0]
                if var not in results:
                    results[var] = r
                else:
                    results[var].append(r[-1])
    logger.debug('time-distance analysis finished')
    return results


def get_average(subjects):
    """Get averaged timedist for normal condition"""
    if not isinstance(subjects, list):
        subjects = [subjects]
    logger.debug('starting time-distance analysis')
    ans = list()
    for j, subject in enumerate(subjects):
        logger.debug('processing subject %s' % subject)
        Nfiles = get_files(subject, 'normal')
        ans.extend([analysis.get_analysis(c3dfile) for c3dfile in Nfiles])
    return analysis.group_analysis(ans)
    
    
    


