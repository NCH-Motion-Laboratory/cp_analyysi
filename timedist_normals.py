# -*- coding: utf-8 -*-
"""
CP project:
compute normal data from CP project normal subjects

@author: Jussi (jnu@iki.fi)
"""

import json

import cp_walk_parameters
from gaitutils.viz import plot_matplotlib, plot_misc

subjects = ['TD22', 'TD23']
outf = 'timedist_normals.json'

ana_mean, ana_std = cp_walk_parameters.get_timedist_average(subjects)


maxes = dict()
for var, di in ana_mean['unknown'].items():
    val = (di['Left'] + di['Right'])/2.
    maxes[var] = val


fig = plot_matplotlib.time_dist_barchart(ana_mean, stddev=ana_std, maxes=maxes)
plot_misc.show_fig(fig)

with open(outf, 'w') as f:
    json.dump(maxes, f)
    
    

    

