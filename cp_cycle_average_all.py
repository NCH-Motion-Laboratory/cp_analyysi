# -*- coding: utf-8 -*-
"""

CP-projektin analyysiskripti
vertaile keskiarvoja norm vs kognitiivinen
kaikki trialit / koehlöt


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

    
def _do_average(subjects, side):

    # parameters
    rootdir = 'Z:\\Userdata_Vicon_Server\\CP-projekti'
    plotdir = "Z:\\CP_projekti_analyysit\\Normal_vs_cognitive"
    max_dist = 15  # deg, for outlier detection

    # special layout
    lout = [['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX'],
            ['PelvisAnglesX', 'PelvisAnglesY', 'PelvisAnglesZ'],
            ['ThoraxAnglesX', 'ThoraxAnglesY', 'ThoraxAnglesZ'], 
            ['ShoulderAnglesX', 'ShoulderAnglesY', 'ShoulderAnglesZ']]
    # add side
    for i, row in enumerate(lout):
        for j, item in enumerate(row):
            lout[i][j] = side+item
    # flatten into list
    lout_ = [item for row in lout for item in row]
    
    Cfiles = list()
    Nfiles = list()
    
    for subject in subjects:
        # try to auto find data dirs under subject dir
        subjdir = op.join(rootdir, subject)
        datadirs = [file for file in os.listdir(subjdir) if
                    op.isdir(op.join(subjdir, file))]
        if len(datadirs) > 1:
            raise Exception('Multiple data dirs under subject')
        datadir = datadirs[0]
        
        # collect normal walk trials
        Nglob = op.join(subjdir, datadir, '*N?_*.c3d')
        Nfiles += glob.glob(Nglob)
        
        # collect cognitive trials
        Cglob = op.join(subjdir, datadir, '*C?_*.c3d')
        Cfiles += glob.glob(Cglob)
                   
        if not (Cfiles and Nfiles):
            raise Exception('No trials for subject %s' % subject)

    print('total of %d/%d trials' % (len(Nfiles), len(Cfiles)))
    
    # average over trials                                    
    models = gaitutils.models.models_all[:2]  # PiG lower and upper
    Cavgdata, Cstddata, C_ok, Ccyc = gaitutils.stats.average_trials(Cfiles, models,
                                                              max_dist=max_dist)
    Navgdata, Nstddata, N_ok, Ncyc = gaitutils.stats.average_trials(Nfiles, models,
                                                              max_dist=max_dist)
    Ntr = gaitutils.trial.AvgTrial(Navgdata)
    Ctr = gaitutils.trial.AvgTrial(Cavgdata)
    
    # plot all
    pl = gaitutils.Plotter()
    pl.layout = lout
    pl.trial = Ntr
    cfg['plot']['model_stddev_alpha'] = '0.2'
    cfg['plot']['model_stddev_colors'] = "{'R': 'blue', 'L': 'blue'}"
    cfg['plot']['model_tracecolors'] = "{'R': 'blue', 'L': 'blue'}"
    
    pl.plot_trial(plot_model_normaldata=False, model_stddev=Nstddata)
       
    cfg['plot']['model_stddev_colors'] = "{'R': 'red', 'L': 'red'}"
    cfg['plot']['model_tracecolors'] = "{'R': 'red', 'L': 'red'}"
    pl.trial = Ctr
    
    maintitle = '%s normal vs cognitive (%s)\n' % (subjects, side)
    maintitle += 'N_cycles normal: %d, cognitive: %d' % (Ncyc[side], Ccyc[side])
                             
    pl.plot_trial(plot_model_normaldata=False, model_stddev=Cstddata,
                  show=True, superpose=True, maintitle=maintitle)
    
    # create custom legend outside axes
    from matplotlib.patches import mlines
    l_norm = mlines.Line2D([], [], color='blue')
    l_cogn = mlines.Line2D([], [], color='red')
    plt.legend([l_norm, l_cogn], ['normal', 'cognitive'], bbox_to_anchor=(.98, .98),
               bbox_transform=plt.gcf().transFigure, fontsize=8)
    
    # create pdf and png figs
    figname = '%s_%s' % (subjects, side)
    figname = op.join(plotdir, figname)
    plt.savefig(figname+'.pdf')
    plt.savefig(figname+'.png')
    logname = figname+'.log'
    
    # report N of cycles per var
    print('\n%s: %s' % (subjects, side))
    print('N of normal cycles per variable:')
    print({key: var for key, var in N_ok.items() if key in lout_})
    print('N of cogn. cycles per variable:')
    print({key: var for key, var in C_ok.items() if key in lout_})
    
    # ...also into logfile
    with open(logname, 'w') as f:
        print('\n%s: %s' % (subjects, side), file=f)
        print('N of normal cycles per variable:', file=f)
        print({key: var for key, var in N_ok.items() if key in lout_}, file=f)
        print('N of cogn. cycles per variable:', file=f)
        print({key: var for key, var in C_ok.items() if key in lout_}, file=f)


side = 'R'
subjects = ['TD26', 'TD25', 'TD24', 'TD23', 'TD17', 'TD04']
_do_average(subjects, side)


