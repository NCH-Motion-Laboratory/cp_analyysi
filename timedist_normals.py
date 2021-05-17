# -*- coding: utf-8 -*-
"""
CP project:
compute normal data from CP project normal subjects

@author: Jussi (jnu@iki.fi)
"""
# %% init
import json
import logging
import numpy as np

from gaitutils.viz import plot_matplotlib, plot_misc, plot_plotly
from gaitutils.envutils import _ipython_setup
from gaitutils import timedist

import cp_walk_parameters
import cp_common


_ipython_setup()
logging.basicConfig(level=logging.INFO)

outf = 'timedist_normals.json'

# %% gather data
# subjects = ['TD22', 'TD23']  # for testing
subjects = cp_common.get_subjects()
timedists = cp_walk_parameters.get_timedist_values(subjects)


# %% filter timedist values and compute mean/std


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


tdists_ok = [tdist for tdist in timedists if _check_timedist(tdist)]

ana_mean = timedist.group_analysis(tdists_ok)
ana_std = timedist.group_analysis(tdists_ok, fun=np.std)


# %% calculate reference values
timedist_refs = dict()
for var, di in ana_mean['unknown'].items():
    # we take mean of left/right as reference
    timedist_refs[var] = (di['Left'] + di['Right']) / 2.0


# %% plot values
fig = plot_plotly.time_dist_barchart(ana_mean, stddev=ana_std, bar_scaling=timedist_refs)
plot_misc.show_fig(fig)
fig = plot_matplotlib.time_dist_barchart(ana_mean, stddev=ana_std, bar_scaling=timedist_refs)
plot_misc.show_fig(fig)


# %% write ref. values
with open(outf, 'w') as f:
    json.dump(timedist_refs, f)
