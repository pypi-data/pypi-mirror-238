import core.antslogger as log
import core.antstimeseries as timeseries
import postprocessing.power as power

import scipy as sp
import numpy as np


class FFT(timeseries.TimeSeries):
    def __init__(self):
        super(FFT, self).__init__()

    def spectrogram(self, **kwargs):
        # kwargs
        samples = kwargs.get('samples') if 'samples' in kwargs else self.samples
        fs = kwargs.get('fs') if 'fs' in kwargs else self.sample_frequency
        seg = kwargs.get('nperseg') if 'nperseg' in kwargs else int(np.floor(len(samples) / 2))
        overlap = kwargs.get('noverlap') if 'noverlap' in kwargs else int(np.floor(seg / 4.5))
        window = kwargs.get('window') if 'window' in kwargs else 'hann'
        nfft = kwargs.get('nfft') if 'nfft' in kwargs else seg
        scaling = kwargs.get('scaling') if 'scaling' in kwargs else 'spectrum'
        mode = kwargs.get('mode') if 'mode' in kwargs else 'complex'

        if 'duration' in kwargs:
            duration_s = kwargs.get('duration')
            if isinstance(duration_s, list):
                duration_ts = [int((dur * fs) - 1) if dur > 0 else 0 for dur in duration_s]
                samples = samples[duration_ts[0]:duration_ts[-1]]  # slicing samples
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                samples = samples  # Default samples
        else:
            samples = samples  # Default samples

        # spectrogram
        freqs, times, spectrum = sp.signal.spectrogram(x=samples, fs=fs, nperseg=seg, noverlap=overlap,
                                                       window=window, nfft=nfft, scaling=scaling, mode=mode)

        # save spectrum
        if 'pscale' in kwargs:
            power_scale = kwargs.get('pscale')
            if isinstance(power_scale, str):
                if power_scale == 'log':
                    self.f_power = np.log10(power.Power.to_freq_power(spectrum))
                else:
                    self.f_power = power.Power.to_freq_power(spectrum)
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                self.f_power = power.Power.to_freq_power(spectrum)
        else:
            self.f_power = power.Power.to_freq_power(spectrum)

        self.waves = spectrum
        self.t_power = power.Power.to_time_power(spectrum)
        self.waves_freqs = freqs
