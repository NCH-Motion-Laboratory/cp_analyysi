# -*- coding: utf-8 -*-
"""

Check the effect of event misplacement on gait curves

@author: Jussi (jnu@iki.fi)
"""

from __future__ import print_function
import gaitutils
from gaitutils import cfg
import matplotlib.pyplot as plt
import numpy as np
import os.path as op


def _delay_events(tr, delay):
    """Delay trial events by delay frames"""
    for li in [tr.lstrikes, tr.rstrikes, tr.ltoeoffs,
               tr.rtoeoffs]:
        for k, it in enumerate(li):
            li[k] = it + delay
    tr.cycles = list(tr._scan_cycles())

rootdir = 'z:/CP_projekti_analyysit'

# read trial and plot
tr = gaitutils.trial.nexus_trial()
pl = gaitutils.Plotter()

pl.layout = [
 ['HipAnglesX', 'HipAnglesZ'],
 ['KneeAnglesX', 'KneeAnglesZ'],
 ['AnkleAnglesX', 'AnkleAnglesZ'],
 [None, None]]

cycs = {'R': 2}
pl.plot_trial(tr, plot_model_normaldata=False, model_cycles=cycs,
              model_tracecolor='g')
# get value at foot strike
print(tr['RHipAnglesX'][1][0])
print(tr['RHipAnglesZ'][1][0])

# delay all events by n frames and plot
delay = 2
_delay_events(tr, delay)
pl.plot_trial(tr, plot_model_normaldata=False, superpose=True,
              model_tracecolor='r', model_cycles=cycs)
print(tr['RHipAnglesX'][1][0])
print(tr['RHipAnglesZ'][1][0])

# add the same delay again and plot
_delay_events(tr, delay)
pl.plot_trial(tr, plot_model_normaldata=False, superpose=True,
              model_tracecolor='b', model_cycles=cycs)
print(tr['RHipAnglesX'][1][0])
print(tr['RHipAnglesZ'][1][0])

pl.set_title('')

# hack a bit to get legend
x = 1
y1 = 2
y2 = 3
y3 = 4
fig, ax2 = plt.subplots()
l1, l2, l3 = ax2.plot(x, y1, 'g', x, y2, 'r', x, y3, 'b')
pl.fig.legend((l1, l2, l3), ('Accurate', '2 frame delay', '4 frame delay'), 'lower right')
plt.close(fig)

pl.fig.savefig(op.join(rootdir, 'events_delay.png'))



    

    
    
    
