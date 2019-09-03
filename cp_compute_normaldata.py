# -*- coding: utf-8 -*-
"""
Compute new normaldata from CP project TD files (normal subjects)

@author: Jussi (jnu@iki.fi)
"""

from __future__ import print_function
import numpy as np
import os.path as op
import logging
import datetime

from gaitutils import analysis, c3d, stats, viz, layouts, normaldata, models
from cp_common import get_files, params, get_subjects


logger = logging.getLogger(__name__)


def get_timedist_average(subjects):
    """Get grand average timedist for subjects (normal trials only).
    Returns tuple of timedist (mean, std)"""
    ans = list()
    for j, subject in enumerate(subjects):
        logger.info('processing subject %s' % subject)
        Nfiles = get_files(subject, 'normal')
        ans.extend([analysis.get_analysis(c3dfile) for c3dfile in Nfiles])
    return (analysis.group_analysis(ans),
            analysis.group_analysis(ans, fun=np.std))


def get_model_data(subjects):
    """Average gait model data for subjects"""
    files = list()
    for subject in subjects:
        logger.info('processing subject %s' % subject)
        files.extend(get_files(subject, 'normal'))
    data, nc = stats._collect_model_data(files, fp_cycles_only=False)
    return data, nc


def get_emg_data(subjects, newer_than=None):
    """Average gait model data for subjects"""
    files = list()
    for subject in subjects:
        logger.info('processing subject %s' % subject)
        files.extend(get_files(subject, 'normal', newer_than=newer_than))
    data = stats._collect_emg_data(files, grid_points=101)
    return data


# ages for TD subjects
age_di = {'TD01':	13.1,
          'TD02':	12.2,
          'TD03':	12.2,
          'TD04':	14.3,
          'TD05':	15.9,
          'TD07':	11.6,
          'TD08':	16.7,
          'TD09':	11.6,
          'TD10':	12.3,
          'TD11':	13.8,
          'TD12':	17.6,
          'TD13':	17.3,
          'TD17':	17.3,
          'TD20':	13.5,
          'TD21':	16.0,
          'TD22':	11.8,
          'TD23':	11.6,
          'TD24':	13.9,
          'TD25':	11.9,
          'TD26':	10.1,
          'TD28':	13.6,
          'TD29':	14.2,
          'TD30':	14.1,
          'TD31':	11.1,
          'TD32':	12.2,
          'TD34':	11.6,
          'TD35':	10.4,
          'TD37':	12.8,
          'TD38':	10.9,
          'TD70':	16.3,
          'TD77':	16.8,
          'TD82':	13.3}
age_cutoff = None
# sessions must be newer than this
newer_than = datetime.datetime(2018, 3, 1)


# compute new normal data
if __name__ == '__main__' and False:
    logging.basicConfig(level=logging.INFO)
    if age_cutoff:
        subjects = get_subjects()
        subjects = [x for x in subjects if age_di[x] < age_cutoff]
    else:
        subjects = params['analysis_subjects'] or get_subjects()
    logger.debug('subjects: %s' % subjects)
    # get all data as numpy arrays
    data, nc = get_model_data(subjects)
    ndata = normaldata.normals_from_data(data)
    fn = op.join(params['plotdir'], 'TD_normaldata_12andbelow.xlsx')
    normaldata._write_xlsx(ndata, fn)


if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    if age_cutoff:
        subjects = get_subjects()
        subjects = [x for x in subjects if age_di[x] < age_cutoff]
    else:
        subjects = params['analysis_subjects'] or get_subjects()
    logger.info('subjects: %s' % subjects)
    # get all data as numpy arrays
    data, meta = get_emg_data(subjects, newer_than=newer_than)
    plt.figure()
    ch = 'RSol'
    plt.plot(data[ch].T)
    plt.plot(np.median(data[ch], axis=0), 'k--')
    plt.title(ch)

    emg_normals = dict()
    chs = (x[1:] for x in data.keys())  # strip context
    for ch_ in chs:
        plt.figure()
        rch, lch = 'R'+ch_, 'L'+ch_
        emg_normals[ch] = np.median(data[rch], axis=0) + np.median(data[lch], axis=0)
        emg_normals[ch] /= emg_normals[ch].max()
        plt.imshow(emg_normals[ch][None, :], aspect="auto")
        plt.colorbar()
        plt.title(ch_)
        plt.axis('off')
        

# comparison with old normaldata
"""        
    ndata_base = normaldata.read_all_normaldata()
    for var in ndata_base:
        if var not in ndata:
            continue
        plt.figure()
        plt.plot(ndata_base[var][:, 0], 'b-')
        plt.plot(ndata_base[var][:, 1], 'r-')        
        plt.plot(ndata[var][:, 0], 'b--')
        plt.plot(ndata[var][:, 1], 'r--')
        plt.title(var)
"""


# plot all data and median for given variable
"""     
var = 'AnkleMomentX'
rvar, lvar = 'R'+var, 'L'+var
rcurves, lcurves = data[rvar], data[lvar]
curves = np.concatenate([rcurves, lcurves])
plt.figure()
plt.plot(curves.T)
plt.plot(np.median(curves, axis=0), 'k-')

""" 

# effect of age cutoff
"""
ndata_all = normaldata.read_normaldata(r"D:\CP gait data cleaned\TD\TD_normaldata_all.xlsx")
ndata_12 = normaldata.read_normaldata(r"D:\CP gait data cleaned\TD\TD_normaldata_12andbelow.xlsx")
for var in models.pig_lowerbody.varlabels_noside:
    if var not in ndata_all:
        continue
    plt.figure()
    plt.plot(ndata_all[var][:, 0], 'b-')
    plt.plot(ndata_all[var][:, 1], 'r-')        
    plt.plot(ndata_12[var][:, 0], 'b--')
    plt.plot(ndata_12[var][:, 1], 'r--')
    plt.title(var)        
"""
        

# effect of age cutoff

"""
ndata_old = normaldata.read_normaldata(r"Z:\PXD_files\muscle_length_13_19.xlsx")
ndata_new = normaldata.read_normaldata(r"Z:\PXD_files\TD_normaldata_all.xlsx")

for var in models.musclelen.varlabels_noside:
    if var not in ndata_new:
        continue
    plt.figure()
    plt.plot(ndata_old[var][:, 0], 'b-')
    plt.plot(ndata_old[var][:, 1], 'r-')        
    plt.plot(ndata_new[var][:, 0], 'b--')
    plt.plot(ndata_new[var][:, 1], 'r--')
    plt.title(var)        
"""     
    
    
