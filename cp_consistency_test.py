# -*- coding: utf-8 -*-
"""

CP-project:
check trial data by overlay

@author: Jussi (jnu@iki.fi)
"""


import gaitutils
from cp_common import get_files


def _onpick(ev):
    a = ev.artist
    print '%s: cycle %s/%d' % (a._trialname, a._cycle.context, a._cycle.index)


subject = 'TD26'
cond = 'normal'

files = get_files(subject, cond)

pl = gaitutils.Plotter()

vars = [['HipAnglesX', 'KneeAnglesX', 'AnkleAnglesX'],
        ['PelvisAnglesX', 'PelvisAnglesY', 'PelvisAnglesZ'],
        ['ThoraxAnglesX', 'ThoraxAnglesY', 'ThoraxAnglesZ'],
        ['ShoulderAnglesX', 'ShoulderAnglesY', 'ShoulderAnglesZ']]

pl.layout = vars
cant_read = list()

for fn in files[:5]:
    pl.open_trial(fn)
    # check if model vars can be read
    try:
        pl.trial['LHipAnglesX']
    except (gaitutils.GaitDataError, KeyError):
        cant_read.append(fn)
        continue
    pl.plot_trial(model_cycles='all', show=False, superpose=True,
                  model_alpha=.5)

pl.set_title('%s: %s (%d files)' % (subject, cond, len(files)))

pl.fig.canvas.mpl_connect('pick_event', _onpick)

pl.show()

if cant_read:
    print 'could not read: %s' % cant_read

