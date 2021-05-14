# -*- coding: utf-8 -*-
"""
CP project:
compute normal data from CP project normal subjects

@author: Jussi (jnu@iki.fi)
"""
# %% init
import json
import logging

from gaitutils.viz import plot_matplotlib, plot_misc
from gaitutils.envutils import _ipython_setup

import cp_walk_parameters


_ipython_setup()
logging.basicConfig(level=logging.DEBUG)


# %% foo
subjects = ['TD22', 'TD23']
outf = 'timedist_normals.json'

ana_mean, ana_std = cp_walk_parameters.get_timedist_average(subjects)


maxes = dict()
for var, di in ana_mean['unknown'].items():
    val = (di['Left'] + di['Right']) / 2.0
    maxes[var] = val


fig = plot_matplotlib.time_dist_barchart(ana_mean, stddev=ana_std)
plot_misc.show_fig(fig)

with open(outf, 'w') as f:
    json.dump(maxes, f)
