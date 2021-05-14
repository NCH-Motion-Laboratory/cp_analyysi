# -*- coding: utf-8 -*-
"""
CP project:
compute normal data from CP project normal subjects

@author: Jussi (jnu@iki.fi)
"""
# %% init
import enum
import json
import logging

from gaitutils.viz import plot_matplotlib, plot_misc, plot_plotly
from gaitutils.envutils import _ipython_setup

import cp_walk_parameters


_ipython_setup()
logging.basicConfig(level=logging.DEBUG)


# %% foo
subjects = ['TD22', 'TD23']
outf = 'timedist_normals.json'

ana_mean, ana_std = cp_walk_parameters.get_timedist_average(subjects)


# %% maxes
maxes = dict()
rng = np.linspace(.25, 1, 12)
k = 0
for var, di in ana_mean['unknown'].items():
    val = (di['Left'] + di['Right']) / 2.0
    maxes[var] = val / rng[k]
    k += 1
maxes.pop('Stride Time')

# %% foo2
fig = plot_plotly.time_dist_barchart(ana_mean, stddev=ana_std, bar_scaling=maxes)
plot_misc.show_fig(fig)
fig = plot_matplotlib.time_dist_barchart(ana_mean, stddev=ana_std, bar_scaling=maxes)
plot_misc.show_fig(fig)

#with open(outf, 'w') as f:
#    json.dump(maxes, f)


# %%
import numpy as np

a = np.array([1,2,3,4])

b = np.array([10,20,30,np.nan])

foo = [x if not np.isnan(x) else a[k] for k, x in enumerate(b)]

