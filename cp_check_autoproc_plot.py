# -*- coding: utf-8 -*-
"""
CP, check autoproc results

Create plots

@author: Jussi (jnu@iki.fi)
"""

from __future__ import division
import os.path as op
import pandas
import matplotlib.pyplot as plt


# results shall be entered into this workbook
rootdir = 'z:/CP_projekti_analyysit'
xls_filename = 'z:/CP_projekti_analyysit/cp_autoproc_check_final.xlsx'

data = pandas.read_excel(xls_filename)

trial = data.trial
notes = data.notes

ev_counts = data.events.value_counts()
fp_counts = data.fp.value_counts()
N = len(data.events)

n_gaps = ev_counts.g
n_label_failures = ev_counts.l

n_preproc_ok = N - (n_gaps + n_label_failures)
n_evs_ok = ev_counts.x / n_preproc_ok  # within 2 frames
n_fp_ok = fp_counts.x / n_preproc_ok

labels = ['Labelling failure', 'Unfillable gaps', 'Preprocessing OK']
sizes = [n_gaps, n_label_failures, n_preproc_ok]
explode = (.05, .05, .05)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
p, t, a = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                  startangle=0, colors=['pink', 'r', 'g'],
                  explode=explode)
# wedgeprops={'linewidth': 1, 'edgecolor': 'k'},

for l in a+t:
    l.set_fontsize(10)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.savefig(op.join(rootdir, 'preproc_pie.png'))

plt.show()
