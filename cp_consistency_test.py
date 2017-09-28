# -*- coding: utf-8 -*-
"""

Test consistency of CP trials

@author: Jussi (jnu@iki.fi)
"""


import gaitutils
import matplotlib.pyplot as plt
import glob
import numpy as np


# get files
fnp = 'Z:\\Userdata_Vicon_Server\\CP-projekti\\TD25\\2017_5_11\\*_N*c3d'
files = glob.glob(fnp)


pl = gaitutils.Plotter()


vars = [['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX'],
        ['PelvisAnglesX', 'PelvisAnglesY', 'PelvisAnglesZ'],
        ['ThoraxAnglesX', 'ThoraxAnglesY', 'ThoraxAnglesZ'], 
        ['ShoulderAnglesX', 'ShoulderAnglesY', 'ShoulderAnglesZ']]

pl.layout = vars


for fn in files:

    pl.open_trial(fn)

    if pl.trial.cycles:
        pl.plot_trial(model_cycles='all', show=False, superpose=True,
                      model_alpha=.5)
    else:
        print 'no cycles for %s' % fn

pl.show()





