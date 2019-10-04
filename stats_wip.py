# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:36:28 2019

@author: vicon123
"""



import numpy as np
import matplotlib.pyplot as plt


def mad(x, scale=1.4826, axis=0):
    """Median absolute deviation. A robust alternative to stddev."""
    med = np.median(x, axis=axis)
    return scale * np.median(np.abs(x - med), axis=axis)


def zscore(x, axis=0):
    mean = np.mean(x, axis=axis)
    std = np.std(x, axis=axis)
    return (x - mean) / std


def robust_zscore(x, axis=0):
    """Compute robust Z-score for data, using median statistics"""
    xmedian = np.median(x, axis=axis)
    xmad = mad(x, axis=axis)
    return (x - xmedian) / xmad
    

def outliers(x, axis=0, threshold=4):
    rzs = robust_zscore(x, axis=axis)
    return np.where(abs(rzs) > threshold)[axis]
    

# want to reject 1/1000 curves by chance

A = 50
nA = 5  # noise amplitude
nt = 100
nsig = 200
t = np.linspace(0, 1, num=nt)
f = 20
f = A * np.sin(2*np.pi*f*t)

noise = np.random.randn(nsig, nt) * nA
noisyf = f + noise
# create outlier
noisyf[0, int(nt/2)] += 30

plt.figure()
plt.plot(noisyf.T)
plt.title('data')

plt.figure()
plt.plot(zscore(noisyf).T)
plt.title('regular Z')

plt.figure()
plt.plot(robust_zscore(noisyf).T)
plt.title('robust Z')

