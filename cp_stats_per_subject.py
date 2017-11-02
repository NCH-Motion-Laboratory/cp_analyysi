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
import scipy

def _get_data(subject):
    """Average trials for a given subject, separately for cogn / normal"""
        
    # parameters
    rootdir = 'Z:\\Userdata_Vicon_Server\\CP-projekti'
    plotdir = "Z:\\CP_projekti_analyysit\\Normal_vs_cognitive"
  
    Cfiles = list()
    Nfiles = list()

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

    print('%s: total of %d/%d trials' % (subject, len(Nfiles), len(Cfiles)))
    
    C_avgdata, C_stddata, _, _ = gaitutils.stats.average_trials(Cfiles)
    N_avgdata, N_stddata, _, _ = gaitutils.stats.average_trials(Nfiles)

    return N_avgdata, N_stddata, C_avgdata, C_stddata
    
    
def _get_vars(N_avgdata, C_avgdata):
    """Compute variables of interest from averaged data"""
    
    results = dict()
    results['C'] = dict()
    results['N'] = dict()

    stats_vars = ['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX',
                  'ThoraxAnglesY', 'ThoraxAnglesZ']

    for cond in results.keys():
        for varname_ in stats_vars:
            for side in ['R', 'L']:
                varname = side + varname_
                results[cond][varname] = dict()
                data = C_avgdata if cond == 'C' else N_avgdata
                # data at first frame (foot strike)
                results[cond][varname]['at_foot_strike'] = data[varname][0]
                # maximum for each curve
                results[cond][varname]['max'] = data[varname].max()
                # minimum for each curve
                results[cond][varname]['min'] = data[varname].min()
                # local extrema for each curve
                xind = scipy.signal.argrelextrema(data[varname], np.greater)[0]
                results[cond][varname]['localextind'] = xind
                results[cond][varname]['localext'] = data[varname][xind]
                xind_contact = xind[np.where(xind < 60)]
                results[cond][varname]['contact_max'] = data[varname][xind_contact]
                
    return results


subjects = ['TD26', 'TD25', 'TD24', 'TD23', 'TD17', 'TD04']
subject = subjects[0]

N_avgdata, N_stddata, C_avgdata, C_stddata = _get_data(subject)

res = _get_vars(N_avgdata, C_avgdata)

y = res['C']['LHipAnglesX']['foot_strike']



