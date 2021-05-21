# -*- coding: utf-8 -*-
"""
CP project: look at timedist normal data from TD subjects

@author: Jussi (jnu@iki.fi)
"""

# %% init
import json
import logging
import gaitutils
import numpy as np

from gaitutils.viz import plot_matplotlib, plot_misc, plot_plotly
from gaitutils.envutils import _ipython_setup
from gaitutils import timedist

import cp_walk_parameters
import cp_common



def _check_timedist(tdist):
    """Check if all the timedist values exist"""
    for var in cp_walk_parameters.vars:
        for context in ['Left', 'Right']:
            if (
                context not in tdist['unknown'][var]
                or not tdist['unknown'][var][context]
            ):
                return False
    return True


_ipython_setup()
logging.basicConfig(level=logging.INFO)

outf = 'timedist_normals.json'

# %% gather data
# subjects = ['TD22', 'TD23']  # for testing
subjects = cp_common.get_subjects()
timedists_, filenames_ = cp_walk_parameters.get_timedist_values(subjects)
# filter out timedists w/ missing values
timedists_files = [(tdist, fname) for tdist, fname in zip(timedists_, filenames_) if _check_timedist(tdist)]
timedists, filenames = zip(*timedists_files)


# %% get data for single var (combine L/R)
import gaitutils
import scipy

datas = dict()
for var in cp_walk_parameters.vars:
    datas[var] = np.array([
        di['unknown'][var][context] for di in timedists for context in ['Left', 'Right']
    ])
    files_this = np.array([fn for fn in filenames for context in ['Left', 'Right']])
    print(f'{var=}')
    med = np.nanmedian(datas[var])
    print(f'{med=}')
    # calculate 'robust std'
    mad = scipy.stats.median_abs_deviation(datas[var], scale='normal', nan_policy='omit')
    print(f'{mad=}')
    dev = np.abs(datas[var] - med) / mad
    outliers = np.where(dev > 5)[0]
    if np.any(outliers):
        print(f'{datas[var][outliers]=}')
        print(f'{files_this[outliers]=}')




# %% find timedist data with weird cadence values (exactly 120)
weird_cads = [
    (t['unknown'], f)
    for t, f in zip(timedists, filenames)
    if 'Right' in t['unknown']['Cadence'] and (t['unknown']['Cadence']['Right'] == 120.0 or t['unknown']['Cadence']['Left'] == 120.0)
]

# %% filter timedists




# %% some stats
import matplotlib.pyplot as plt

for var in cp_walk_parameters.vars:
    data = [
        di['unknown'][var][context] for di in timedists for context in ['Left', 'Right']
    ]
    plt.figure()
    plt.hist(data, bins=30)
    plt.title(var)


# %% mean/stddev
ana_median = timedist.group_analysis(timedists, fun=np.median)
ana_std = timedist.group_analysis(timedists, fun=np.std)


# %% calculate reference values
timedist_refs = dict()
for var, di in ana_mean['unknown'].items():
    # we take mean of left/right as reference
    timedist_refs[var] = (di['Left'] + di['Right']) / 2.0


# %% plot values
fig = plot_plotly.time_dist_barchart(
    ana_mean, stddev=ana_std, bar_scaling=timedist_refs
)
plot_misc.show_fig(fig)
fig = plot_matplotlib.time_dist_barchart(
    ana_mean, stddev=ana_std, bar_scaling=timedist_refs
)
plot_misc.show_fig(fig)


# %% write ref. values
with open(outf, 'w') as f:
    json.dump(timedist_refs, f)
