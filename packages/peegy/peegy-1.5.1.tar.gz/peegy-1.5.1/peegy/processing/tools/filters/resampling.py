import numpy as np
import multiprocessing
import pyfftw
import astropy.units as u
from tqdm import tqdm
from .. multiprocessing.multiprocessesing_filter import filt_data
from .. filters.eegFiltering import bandpass_fir_win
__author__ = 'jundurraga'


def eeg_resampling(x: np.array = np.array([]),
                   new_fs: u.Quantity = None,
                   fs: u.Quantity = None,
                   transition_width: u.Quantity = 1.0 * u.Hz,
                   blocks=8) -> np.array:
    factor = new_fs / fs
    if factor == 1.0:
        return x, factor
    _original_time = x.shape[0] / fs
    updated_nfft = int(_original_time * new_fs)
    if factor < 1:
        _b = bandpass_fir_win(high_pass=None,
                              low_pass=new_fs / 2 - transition_width,
                              fs=fs,
                              transition_width=transition_width)
        _b = _b * u.dimensionless_unscaled
        # apply antialiasing
        x = filt_data(data=x, b=_b)

    blocks = np.minimum(x.shape[1], blocks)
    xfilt = np.zeros((updated_nfft, x.shape[1]))
    for b in tqdm(np.arange((np.ceil(x.shape[1]) / blocks)), desc='Resampling'):
        pos_ini = int(b * blocks)
        pos_end = int(np.minimum((b + 1) * blocks, x.shape[1]) + 1)
        fft = pyfftw.builders.rfft(x[:, pos_ini:pos_end],
                                   overwrite_input=False,
                                   planner_effort='FFTW_ESTIMATE',
                                   axis=0,
                                   threads=multiprocessing.cpu_count())
        fft_data = fft()
        ifft = pyfftw.builders.irfft(fft_data,
                                     n=updated_nfft,
                                     overwrite_input=False,
                                     planner_effort='FFTW_ESTIMATE',
                                     axis=0,
                                     threads=multiprocessing.cpu_count())
        sub_set = ifft()
        xfilt[:, pos_ini:pos_end] = sub_set
        if pos_end == x.shape[1]:
            break
    return xfilt * factor * x.unit, factor
