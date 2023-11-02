import numpy as np
from peegy.processing.tools.filters.resampling import eeg_resampling
import matplotlib.pyplot as plt
import astropy.units as u
import matplotlib
if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
    matplotlib.use('Qt5Agg')

__author__ = 'jundurraga-ucl'


fs = 1000.0 * u.Hz
f_s = 25.0 * u.Hz
n_o = 717.0
t = np.arange(0, n_o) / fs
y1 = np.sin(2 * np.pi * u.rad * f_s * t + np.pi * u.rad / 2) * u.uV
y2 = np.sin(2 * np.pi * u.rad * 5 * f_s * t) * u.uV
y = np.tile(np.array(y1 + y2) + 0.0 * np.random.random(t.shape), (4, 1)).T * u.uV
new_fs = 5000 * u.Hz

yf = np.fft.fft(y, axis=0)
freq = np.arange(len(yf)) * fs / len(yf)
yc, factor = eeg_resampling(x=y, new_fs=new_fs, fs=fs, blocks=8)
new_fs = fs * factor
new_time = np.arange(0, yc.shape[0]) / new_fs
plt.plot(t, y, label='original', color='b')
plt.plot(t, y, 'bo')
plt.plot(t, y1, label='h1')
plt.plot(t, y2, label='h2')
plt.plot(np.squeeze(new_time), np.squeeze(yc), 'r', label='resampled')
plt.plot(np.squeeze(new_time), np.squeeze(yc), 'rv', label='resampled')
plt.legend()
plt.show()
plt.show()
