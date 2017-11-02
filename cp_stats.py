# -*- coding: utf-8 -*-
"""

CP-projektin analyysiskripti
numeerista dataa, norm vs kognitiivinen
kaikki trialit / koehlöt


erikseen norm/kognitiivinen
erikseen oikea/vasen puoli

muuttujat:

    hip flexion:
    strike, toeoff
    
knee flexion:
    strike
    maksimi ekan puoliskon ajalta (derivaatan nollakohta)
    
ankle dorsi/plant:
    strike, toeoff
    kontaktivaiheen aik. maksimi
    
thorax lateral flex:
    max, min
    
thorax rotation:
    max, min



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

    
def _get_stats(subjects):

    # parameters
    rootdir = 'Z:\\Userdata_Vicon_Server\\CP-projekti'
    plotdir = "Z:\\CP_projekti_analyysit\\Normal_vs_cognitive"

    stats_vars = ['HipAnglesX', 'PelvisAnglesX', 'AnkleAnglesX',
                  'ThoraxAnglesY', 'ThoraxAnglesZ']
    
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
    
    C_data, C_nc = gaitutils.stats._collect_model_data(Cfiles)
    N_data, N_nc = gaitutils.stats._collect_model_data(Nfiles)
    
    results = dict()
    results['C'] = dict()
    results['N'] = dict()

    for cond in results.keys():
        for varname in stats_vars:
            print('collect %s' % varname)
            sys.stdout.flush()
            results[cond][side+varname] = dict()
            # data at first frame (foot strike)
            results[cond][side+varname]['foot_strike'] = C_data[varname][:, 0]
        
    return results


subjects = ['TD26', 'TD25', 'TD24', 'TD23', 'TD17', 'TD04'][:2]
res = _get_stats(subjects)


