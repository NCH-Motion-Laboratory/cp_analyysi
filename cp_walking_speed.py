# -*- coding: utf-8 -*-
"""

-keskiarvo per 10:n blokki
-40 trialin keskiarvo


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
from gaitutils import (nexus, cfg, utils, read_data, eclipse,
                       register_gui_exception_handler, GaitDataError)


def trial_median_velocity(source):
    """ Compute median velocity over whole trial by differentiation of marker
    data """
    MIN_VEL = .1
    try:
        frate = read_data.get_metadata(source)['framerate']
        dim = utils.principal_movement_direction(source, cfg.autoproc.
                                                 track_markers)
        mkr = cfg.autoproc.track_markers[0]
        vel_ = read_data.get_marker_data(source, mkr)[mkr+'_V'][:, dim]
    except (GaitDataError, ValueError):
        return np.nan
    vel = np.median(np.abs(vel_[np.where(vel_)]))
    vel_ms = vel * frate / 1000.
    return vel_ms if vel_ms >= MIN_VEL else np.nan

    
def _do_velocity_plot(subject):

    # parameters
    rootdir = 'Z:\\Userdata_Vicon_Server\\CP-projekti'
    plotdir = "Z:\\CP_projekti_analyysit\\Normal_vs_cognitive"

    # try to auto find data dirs under subject dir
    subjdir = op.join(rootdir, subject)
    datadirs = [file for file in os.listdir(subjdir) if
                op.isdir(op.join(subjdir, file))]
    if len(datadirs) > 1:
        raise Exception('Multiple data dirs under subject')
    datadir = datadirs[0]
    
    fileglob = op.join(subjdir, datadir, '*.c3d')
    files = glob.glob(fileglob)
   
    print('%s:\n' % subject)
    print(files)
    
    def _autolabel_ctr(rects):
        """
        Attach a text label on each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2., rect.get_y() + .5*height,
                    '%.3f' % height, ha='center', va='center',
                    rotation=90, fontsize=10)

    def _collect_block_vels(block, files):
        """ Get mean and stddev of block velocities. Block is given as
        substring to match, e.g. '_N1_' """
        block_trials = [tr for tr in files if block.upper() in
                        op.splitext(op.split(tr)[1])[0].upper()]  # yay
        block_vels = [trial_median_velocity(file) for file in block_trials]
        print('block %s:' % block)
        print('matched trials: %s' % [op.split(f)[1] for f in block_trials])
        print('trial velocities: %s' % block_vels)
        block_vels = np.array(block_vels)
        block_vels = block_vels[~np.isnan(block_vels)]
        return block_vels.mean(), block_vels.std()

    N_blocks = ['N%d' % (j+1) for j in range(4)]
    N_mean_block_vel, N_std_block_vel = zip(*[_collect_block_vels(block, files)
                                              for block in N_blocks])

    C_blocks = ['C%d' % (j+1) for j in range(4)]
    C_mean_block_vel, C_std_block_vel = zip(*[_collect_block_vels(block, files)
                                              for block in C_blocks])
      
    print(N_mean_block_vel)
    print(C_mean_block_vel)    
    
    ind = np.arange(4)  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig, ax = plt.subplots()
    barsep = .01  # between bars for same block
    rects1 = ax.bar(ind - barsep, N_mean_block_vel, width, color='lightblue',
                    yerr=N_std_block_vel)
    rects2 = ax.bar(ind + barsep + width, C_mean_block_vel, width, color='red',
                    yerr=C_std_block_vel)
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean velocity (m/s)')
    ax.set_title('Trial velocity normal vs. cognitive, subject %s' % subject)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('1', '2', '3', '4'))
    ax.set_xlabel('Block')
    
    ax.legend((rects1[0], rects2[0]), ('Normal', 'Cognitive'))
    _autolabel_ctr(rects1)
    _autolabel_ctr(rects2)
    lims = ax.get_ylim()
    ax.set_ylim([0, lims[1]+.15])
    
    # create pdf and png figs
    figname = '%s_velocity' % subject
    figname = op.join(plotdir, figname)
    plt.savefig(figname+'.pdf')
    plt.savefig(figname+'.png')


subjects = ['TD26', 'TD25', 'TD24', 'TD23', 'TD17', 'TD04', 'DP03']

for subject in subjects:
    _do_velocity_plot(subject)
    
    


