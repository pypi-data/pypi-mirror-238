import os
import warnings
from joblib import Parallel, delayed, cpu_count

import numpy as np
import math
from scipy.signal.windows import dpss
from scipy.signal import detrend

import matplotlib.pyplot as plt

import core.antstimeseries as timeseries


class Multitaper(timeseries.TimeSeries):
    def __init__(self):
        super(Multitaper, self).__init__()

    def multitaper(self, **kwargs):
        # variables
        data = self.samples
        fs = kwargs.get('fs') if 'fs' in kwargs else self.sample_frequency
        frequency_range = kwargs.get('frange') if 'frange' in kwargs else [0, 200]
        time_bandwidth = kwargs.get('tbandwidth') if 'tbandwidth' in kwargs else 3
        num_tapers = kwargs.get('num_tapers') if 'num_tapers' in kwargs else 5
        window_params = kwargs.get('window_params') if 'window_params' in kwargs else [4, 1]
        min_nfft = kwargs.get('min_nfft') if 'min_nfft' in kwargs else 0
        detrend_opt = kwargs.get('detrend_opt') if 'detrend_opt' in kwargs else 'constant'
        multiprocess = kwargs.get('multiprocess') if 'multiprocess' in kwargs else True
        n_jobs = kwargs.get('n_jobs') if 'n_jobs' in kwargs else None
        weighting = kwargs.get('weighting') if 'weighting' in kwargs else 'unity'
        plot_on = kwargs.get('plot_on') if 'plot_on' in kwargs else True
        return_fig = kwargs.get('return_fig') if 'return_fig' in kwargs else False
        save_fig = kwargs.get('save_fig') if 'save_fig' in kwargs else True
        directory = kwargs.get('directory') if 'directory' in kwargs else os.path.join(os.path.dirname(os.getcwd()),
                                                                                       'figures')
        clim_scale = kwargs.get('clim_scale') if 'clim_scale' in kwargs else False
        verbose = kwargs.get('verbose') if 'verbose' in kwargs else True
        xyflip = kwargs.get('xyflip') if 'xyflip' in kwargs else False
        ax = kwargs.get('ax') if 'ax' in kwargs else None

        # pre-processing
        [data, fs, frequency_range, time_bandwidth, num_tapers,
         winsize_samples, winstep_samples, window_start,
         num_windows, nfft, detrend_opt, plot_on, verbose] = self.process_input(frequency_range, time_bandwidth,
                                                                                num_tapers, window_params, min_nfft,
                                                                                detrend_opt, plot_on, verbose)

        # set multitaper parameters
        [window_idxs, stimes, sfreqs, freq_inds] = self.process_spectrogram_params(fs, nfft, frequency_range,
                                                                                   window_start, winsize_samples)
        # split data into segments
        data_segments = data[window_idxs]

        # COMPUTE THE MULTITAPER SPECTROGRAM
        #     STEP 1: Compute DPSS tapers based on desired spectral properties
        #     STEP 2: Multiply the data segment by the DPSS Tapers
        #     STEP 3: Compute the spectrum for each tapered segment
        #     STEP 4: Take the mean of the tapered spectra

        # compute DPSS tapers (STEP 1)
        dpss_tapers, dpss_eigen = dpss(winsize_samples, time_bandwidth, num_tapers, return_ratios=True)
        dpss_eigen = np.reshape(dpss_eigen, (num_tapers, 1))

        # pre-compute weights
        if weighting == 'eigen':
            wt = dpss_eigen / num_tapers
        elif weighting == 'unity':
            wt = np.ones(num_tapers) / num_tapers
            wt = np.reshape(wt, (num_tapers, 1))  # reshape as column vector
        else:
            wt = 0

        # Set up calc_mts_segment() input arguments
        mts_params = (dpss_tapers, nfft, freq_inds, detrend_opt, num_tapers, dpss_eigen, weighting, wt)

        if multiprocess:  # use multiprocessing
            n_jobs = max(cpu_count() - 1, 1) if n_jobs is None else n_jobs
            mt_spectrogram = np.vstack(Parallel(n_jobs=n_jobs)(delayed(self.calc_mts_segment)(
                data_segments[num_window, :], *mts_params) for num_window in range(num_windows)))

        else:  # if no multiprocessing, compute normally
            mt_spectrogram = np.apply_along_axis(self.calc_mts_segment, 1, data_segments, *mts_params)

        # multiply the data segment by the DPSS tapers (STEP 2)
        # compute the spectrum for each tapered segment (STEP 3)
        # take the mean of the tapered spectra (STEP 4)
        # Compute one-sided PSD spectrum
        mt_spectrogram = mt_spectrogram.T
        dc_select = np.where(sfreqs == 0)[0]
        nyquist_select = np.where(sfreqs == fs / 2)[0]
        select = np.setdiff1d(np.arange(0, len(sfreqs)), np.concatenate((dc_select, nyquist_select)))

        mt_spectrogram = np.vstack([mt_spectrogram[dc_select, :], 2 * mt_spectrogram[select, :],
                                    mt_spectrogram[nyquist_select, :]]) / fs

        # Flip if requested
        if xyflip:
            mt_spectrogram = mt_spectrogram.T

        # Plot multitaper spectrogram
        if plot_on:
            # convert from power to dB
            spect_data = self.nanpow2db(mt_spectrogram)

            # Set x and y axes
            dx = stimes[1] - stimes[0]
            dy = sfreqs[1] - sfreqs[0]
            extent = [stimes[0] - dx, stimes[-1] + dx, sfreqs[-1] + dy, sfreqs[0] - dy]

            # Plot spectrogram
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.get_figure()
            im = ax.imshow(spect_data, extent=extent, aspect='auto')
            fig.colorbar(im, ax=ax, label='PSD (dB)', shrink=0.8)
            ax.set_xlabel("Time (HH:MM:SS)")
            ax.set_ylabel("Frequency (Hz)")
            im.set_cmap(plt.cm.get_cmap('cet_rainbow4'))
            ax.invert_yaxis()

            # Scale colormap
            if clim_scale:
                clim = np.percentile(spect_data, [5, 98])  # from 5th percentile to 98th
                im.set_clim(clim)  # actually change colorbar scale

            if return_fig:
                return mt_spectrogram, stimes, sfreqs, (fig, ax)

            if save_fig:
                fig.savefig(os.path.join(directory, 'multitaper.png'))

        return mt_spectrogram, stimes, sfreqs

    def process_input(self, frequency_range=None, time_bandwidth=5, num_tapers=None, window_params=None, min_nfft=0,
                      detrend_opt='linear', plot_on=True, verbose=True):
        """ Helper function to process multitaper_spectrogram() arguments
                Arguments:
                        data (1d np.array): time series data-- required
                        fs (float): sampling frequency in Hz  -- required
                        frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] (default: [0 nyquist])
                        time_bandwidth (float): time-half bandwidth product (window duration*half bandwidth of main lobe)
                                                (default: 5 Hz*s)
                        num_tapers (int): number of DPSS tapers to use (default: None [will be computed
                                          as floor(2*time_bandwidth - 1)])
                        window_params (list): 1x2 list - [window size (seconds), step size (seconds)] (default: [5 1])
                        min_nfft (int): minimum allowable NFFT size, adds zero padding for interpolation (closest 2^x)
                                        (default: 0)
                        detrend_opt (string): detrend data window ('linear' (default), 'constant', 'off')
                                              (Default: 'linear')
                        plot_on (True): plot results (default: True)
                        verbose (True): display spectrogram properties (default: true)
                Returns:
                        data (1d np.array): same as input
                        fs (float): same as input
                        frequency_range (list): same as input or calculated from fs if not given
                        time_bandwidth (float): same as input or default if not given
                        num_tapers (int): same as input or calculated from time_bandwidth if not given
                        winsize_samples (int): number of samples in single time window
                        winstep_samples (int): number of samples in a single window step
                        window_start (1xm np.array): array of timestamps representing the beginning time for each window
                        num_windows (int): number of windows in the data
                        nfft (int): length of signal to calculate fft on
                        detrend_opt ('string'): same as input or default if not given
                        plot_on (bool): same as input
                        verbose (bool): same as input
        """

        # variables
        data = self.samples
        fs = self.sample_frequency

        # Make sure data is 1 dimensional np array
        if len(data.shape) != 1:
            if (len(data.shape) == 2) & (data.shape[1] == 1):  # if it's 2d, but can be transferred to 1d, do so
                data = np.ravel(data[:, 0])
            elif (len(data.shape) == 2) & (data.shape[0] == 1):  # if it's 2d, but can be transferred to 1d, do so
                data = np.ravel(data.T[:, 0])
            else:
                raise TypeError("Input data is the incorrect dimensions. Should be a 1d array with shape (n,) where n is \
                                the number of data points. Instead data shape was " + str(data.shape))

        # Set frequency range if not provided
        if frequency_range is None:
            frequency_range = [0, fs / 2]

        # Set detrending method
        detrend_opt = detrend_opt.lower()
        if detrend_opt != 'linear':
            if detrend_opt in ['const', 'constant']:
                detrend_opt = 'constant'
            elif detrend_opt in ['none', 'false', 'off']:
                detrend_opt = 'off'
            else:
                raise ValueError("'" + str(detrend_opt) + "' is not a valid argument for detrend_opt. The choices " +
                                 "are: 'constant', 'linear', or 'off'.")
        # Check if frequency range is valid
        if frequency_range[1] > fs / 2:
            frequency_range[1] = fs / 2
            warnings.warn('Upper frequency range greater than Nyquist, setting range to [' +
                          str(frequency_range[0]) + ', ' + str(frequency_range[1]) + ']')

        # Set number of tapers if none provided
        if num_tapers is None:
            num_tapers = math.floor(2 * time_bandwidth) - 1

        # Warn if number of tapers is suboptimal
        if num_tapers != math.floor(2 * time_bandwidth) - 1:
            warnings.warn('Number of tapers is optimal at floor(2*TW) - 1. consider using ' +
                          str(math.floor(2 * time_bandwidth) - 1))

        # If no window params provided, set to defaults
        if window_params is None:
            window_params = [5, 1]

        # Check if window size is valid, fix if not
        if window_params[0] * fs % 1 != 0:
            winsize_samples = round(window_params[0] * fs)
            warnings.warn('Window size is not divisible by sampling frequency. Adjusting window size to ' +
                          str(winsize_samples / fs) + ' seconds')
        else:
            winsize_samples = window_params[0] * fs

        # Check if window step is valid, fix if not
        if window_params[1] * fs % 1 != 0:
            winstep_samples = round(window_params[1] * fs)
            warnings.warn('Window step size is not divisible by sampling frequency. Adjusting window step size to ' +
                          str(winstep_samples / fs) + ' seconds')
        else:
            winstep_samples = window_params[1] * fs

        # Get total data length
        len_data = len(data)

        # Check if length of data is smaller than window (bad)
        if len_data < winsize_samples:
            raise ValueError("\nData length (" + str(len_data) + ") is shorter than window size (" +
                             str(winsize_samples) + "). Either increase data length or decrease window size.")

        # Find window start indices and num of windows
        window_start = np.arange(0, len_data - winsize_samples + 1, winstep_samples)
        num_windows = len(window_start)

        # Get num points in FFT
        if min_nfft == 0:  # avoid divide by zero error in np.log2(0)
            nfft = max(2 ** math.ceil(np.log2(abs(winsize_samples))), winsize_samples)
        else:
            nfft = max(max(2 ** math.ceil(np.log2(abs(winsize_samples))), winsize_samples),
                       2 ** math.ceil(np.log2(abs(min_nfft))))

        return ([data, fs, frequency_range, time_bandwidth, num_tapers,
                 int(winsize_samples), int(winstep_samples), window_start, num_windows, nfft,
                 detrend_opt, plot_on, verbose])

    def process_spectrogram_params(self, fs, nfft, frequency_range, window_start, datawin_size):
        """ Helper function to create frequency vector and window indices
                Arguments:
                     fs (float): sampling frequency in Hz  -- required
                     nfft (int): length of signal to calculate fft on -- required
                     frequency_range (list): 1x2 list - [<min frequency>, <max frequency>] -- required
                     window_start (1xm np array): array of timestamps representing the beginning time for each
                                                  window -- required
                     datawin_size (float): seconds in one window -- required
                Returns:
                    window_idxs (nxm np array): indices of timestamps for each window
                                                (nxm where n=number of windows and m=datawin_size)
                    stimes (1xt np array): array of times for the center of the spectral bins
                    sfreqs (1xf np array): array of frequency bins for the spectrogram
                    freq_inds (1d np array): boolean array of which frequencies are being analyzed in
                                              an array of frequencies from 0 to fs with steps of fs/nfft
            """

        # create frequency vector
        df = fs / nfft
        sfreqs = np.arange(0, fs, df)

        # Get frequencies for given frequency range
        freq_inds = (sfreqs >= frequency_range[0]) & (sfreqs <= frequency_range[1])
        sfreqs = sfreqs[freq_inds]

        # Compute times in the middle of each spectrum
        window_middle_samples = window_start + round(datawin_size / 2)
        stimes = window_middle_samples / fs

        # Get indexes for each window
        window_idxs = np.atleast_2d(window_start).T + np.arange(0, datawin_size, 1)
        window_idxs = window_idxs.astype(int)

        return [window_idxs, stimes, sfreqs, freq_inds]

    def calc_mts_segment(self, data_segment, dpss_tapers, nfft, freq_inds, detrend_opt, num_tapers,
                         dpss_eigen, weighting, wt):
        """ Helper function to calculate the multitaper spectrum of a single segment of data
            Arguments:
                data_segment (1d np.array): One window worth of time-series data -- required
                dpss_tapers (2d np.array): Parameters for the DPSS tapers to be used.
                                           Dimensions are (num_tapers, winsize_samples) -- required
                nfft (int): length of signal to calculate fft on -- required
                freq_inds (1d np array): boolean array of which frequencies are being analyzed in
                                          an array of frequencies from 0 to fs with steps of fs/nfft
                detrend_opt (str): detrend data window ('linear' (default), 'constant', 'off')
                num_tapers (int): number of tapers being used
                dpss_eigen (np array):
                weighting (str):
                wt (int or np array):
            Returns:
                mt_spectrum (1d np.array): spectral power for single window
        """

        # If segment has all zeros, return vector of zeros
        if all(data_segment == 0):
            ret = np.empty(sum(freq_inds))
            ret.fill(0)
            return ret

        if any(np.isnan(data_segment)):
            ret = np.empty(sum(freq_inds))
            ret.fill(np.nan)
            return ret

        # Option to detrend data to remove low frequency DC component
        if detrend_opt != 'off':
            data_segment = detrend(data_segment, type=detrend_opt)

        # Multiply data by dpss tapers (STEP 2)
        tapered_data = np.multiply(np.mat(data_segment).T, np.mat(dpss_tapers.T))

        # Compute the FFT (STEP 3)
        fft_data = np.fft.fft(tapered_data, nfft, axis=0)

        # Compute the weighted mean spectral power across tapers (STEP 4)
        spower = np.power(np.imag(fft_data), 2) + np.power(np.real(fft_data), 2)
        if weighting == 'adapt':
            # adaptive weights - for colored noise spectrum (Percival & Walden p368-370)
            tpower = np.dot(np.transpose(data_segment), (data_segment / len(data_segment)))
            spower_iter = np.mean(spower[:, 0:2], 1)
            spower_iter = spower_iter[:, np.newaxis]
            a = (1 - dpss_eigen) * tpower
            for i in range(3):  # 3 iterations only
                # Calc the MSE weights
                b = np.dot(spower_iter, np.ones((1, num_tapers))) / ((np.dot(spower_iter, np.transpose(dpss_eigen))) +
                                                                     (np.ones((nfft, 1)) * np.transpose(a)))
                # Calc new spectral estimate
                wk = (b ** 2) * np.dot(np.ones((nfft, 1)), np.transpose(dpss_eigen))
                spower_iter = np.sum((np.transpose(wk) * np.transpose(spower)), 0) / np.sum(wk, 1)
                spower_iter = spower_iter[:, np.newaxis]

            mt_spectrum = np.squeeze(spower_iter)

        else:
            # eigenvalue or uniform weights
            mt_spectrum = np.dot(spower, wt)
            mt_spectrum = np.reshape(mt_spectrum, nfft)  # reshape to 1D

        return mt_spectrum[freq_inds]

    def nanpow2db(self, y):
        """ Power to dB conversion, setting bad values to nans
            Arguments:
                y (float or array-like): power
            Returns:
                ydB (float or np array): inputs converted to dB with 0s and negatives resulting in nans
        """

        if isinstance(y, int) or isinstance(y, float):
            if y == 0:
                return np.nan
            else:
                ydB = 10 * np.log10(y)
        else:
            if isinstance(y, list):  # if list, turn into array
                y = np.asarray(y)
            y = y.astype(float)  # make sure it's a float array so we can put nans in it
            y[y == 0] = np.nan
            ydB = 10 * np.log10(y)

        return ydB
