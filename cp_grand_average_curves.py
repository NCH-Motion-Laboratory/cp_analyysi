# -*- coding: utf-8 -*-
"""

CP-projektin analyysiskripti
vertaile keskiarvoja norm vs kognitiivinen

TODO:
    
    nopeusdata mukaan

@author: Jussi (jnu@iki.fi)
"""

from __future__ import print_function
import gaitutils
from gaitutils import cfg
import matplotlib.pyplot as plt
import glob
import numpy as np
import sys
import os
import os.path as op

from cp_common import get_files


def _do_average(subjects, side):
    
    if not isinstance(subjects, list):
        subjects =  [subjects]

    # parameters
    rootdir = 'K:\\CP_projekti_kopio'
    plotdir = "Z:\\CP_projekti_analyysit\\Piia"
    max_files = None # limit c3d files read (for debug)
    max_dist = 25  # deg, for outlier detection

    # special layout
    lout = [['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX'],
            ['PelvisAnglesX', 'PelvisAnglesY', 'PelvisAnglesZ'],
            ['ThoraxAnglesX', 'ThoraxAnglesY', 'ThoraxAnglesZ'], 
            ['ShoulderAnglesX', 'ShoulderAnglesY', 'ShoulderAnglesZ']]
    # add side to layout
    for i, row in enumerate(lout):
        for j, item in enumerate(row):
            lout[i][j] = side+item
    # flatten into list
    lout_ = [item for row in lout for item in row]

    Nfiles_all = list()    
    for subject in subjects:
        Nfiles = get_files(subject, 'normal')

        if not Nfiles:
            raise Exception('No trials for &s' % subject)

        Nfiles_all.extend(Nfiles)

    # average over trials
    Ntr = gaitutils.stats.AvgTrial(Nfiles_all, max_dist=max_dist)
    # plot all
    pl = gaitutils.Plotter()
    pl.layout = lout
    pl.trial = Ntr
    cfg['plot']['model_stddev_alpha'] = '0.2'
    cfg['plot']['model_stddev_colors'] = "{'R': 'blue', 'L': 'blue'}"
    cfg['plot']['model_tracecolors'] = "{'R': 'blue', 'L': 'blue'}"
    pl.plot_trial(plot_model_normaldata=True, model_stddev=Ntr.stddev_data)
    #pl.plot_trial()

   
"""                          
    # create custom legend outside axes
    from matplotlib.patches import mlines
    l_norm = mlines.Line2D([], [], color='blue')
    l_cogn = mlines.Line2D([], [], color='red')
    plt.legend([l_norm, l_cogn], ['normal', 'cognitive'], bbox_to_anchor=(.98, .98),
               bbox_transform=plt.gcf().transFigure, fontsize=8)

    # create pdf and png figs
    figname = '%s_%s' % (subject, side)
    figname = op.join(plotdir, figname)
    plt.savefig(figname+'.pdf')
    plt.savefig(figname+'.png')
    logname = figname+'.log'

    # report N of cycles per var
    print('\n%s: %s' % (subject, side))
    print('N of normal cycles per variable:')
    print({key: var for key, var in N_ok.items() if key in lout_})
    print('N of cogn. cycles per variable:')
    print({key: var for key, var in C_ok.items() if key in lout_})
    
    # ...also into logfile
    with open(logname, 'w') as f:
        print('\n%s: %s' % (subject, side), file=f)
        print('N of normal cycles per variable:', file=f)
        print({key: var for key, var in N_ok.items() if key in lout_}, file=f)
        print('N of cogn. cycles per variable:', file=f)
        print({key: var for key, var in C_ok.items() if key in lout_}, file=f)
"""


subjects = ['DP03', 'DP05', 'DP07', 'DP09', 'DP10']
side = 'R'
_do_average(subjects, side)
