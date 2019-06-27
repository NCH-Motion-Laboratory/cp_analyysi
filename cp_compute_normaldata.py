# -*- coding: utf-8 -*-
"""
Compute new normaldata from CP project TD files (normal subjects)

@author: Jussi (jnu@iki.fi)
"""

from __future__ import print_function
import numpy as np
import logging

from gaitutils import analysis, c3d, stats, viz, layouts
from cp_common import get_files, params


logger = logging.getLogger(__name__)


def get_timedist_average(subjects):
    """Get grand average timedist for subjects (normal trials only).
    Returns tuple of timedist (mean, std)"""
    ans = list()
    for j, subject in enumerate(subjects):
        logger.info('processing subject %s' % subject)
        Nfiles = get_files(subject, 'normal')
        ans.extend([analysis.get_analysis(c3dfile) for c3dfile in Nfiles])
    return analysis.group_analysis(ans), analysis.group_analysis(ans, fun=np.std)
    

def get_model_average(subjects):
    """Average gait model data for subjects"""
    files = list()
    for subject in subjects:
        logger.info('processing subject %s' % subject)
        files.extend(get_files(subject, 'normal'))
    #avgdata, stddata, N_ok, _ = stats.average_trials(files, max_dist=None)
    avgdata = stats.AvgTrial(files)
    return avgdata


logging.basicConfig(level=logging.INFO)
subjects = params['analysis_subjects']
avgdata = get_model_average(subjects)

layout = layouts.get_layout('lb_kin')
fig = viz.plot_plotly.plot_trials(avgdata, layout)
#, model_normaldata={})
viz.plot_misc.show_fig(fig)

