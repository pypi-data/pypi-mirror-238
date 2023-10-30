import os
import matlab
import matlab.engine as me
import numpy as np

import core.antslogger as log
import core.antstimeseries as timeseries
import postprocessing.power as power


class Wavelet(timeseries.TimeSeries):

    def __init__(self):
        super(Wavelet, self).__init__()
        self.PATH_MATLAB_TIMEFREQUENCY = os.path.join(os.path.dirname(os.getcwd()),
                                                      'timefrequency', 'matlab_timefrequency')

    def wavelet(self, **kwargs):
        # internal functions
        def _matlab_wavelet(cwt_samples):
            # Wavelet power spectrum - MATLAB
            matlab_engine = me.start_matlab()  # start matlab engine
            matlab_engine.cd(self.PATH_MATLAB_TIMEFREQUENCY)  # change directory to the custom matlab functions

            cwt_sampling_frequency = matlab.double(self.sample_frequency)  # type casting to matlab double

            # run cwt
            waves, freqs = matlab_engine.pyCwt(cwt_samples, cwt_sampling_frequency, nargout=2)
            return waves, freqs

        waves, freqs = [], []  # pre-declaration

        if 'duration' in kwargs:  # set sample duration
            duration_s = kwargs.get('duration')
            if isinstance(duration_s, list):
                duration_ts = [int((dur * self.sample_frequency) - 1) if dur > 0 else 0 for dur in duration_s]
                # slicing and type casting to matlab double
                cwt_samples = matlab.double(self.samples[duration_ts[0]:duration_ts[-1]].tolist())
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                cwt_samples = matlab.double(self.samples.tolist())  # type casting to matlab double
        else:
            cwt_samples = matlab.double(self.samples.tolist())  # type casting to matlab double

        if 'operation' in kwargs:
            operation = kwargs.get('operation')
            if isinstance(operation, str):
                if operation == 'matlab':
                    waves, freqs = _matlab_wavelet(cwt_samples=cwt_samples)  # run matlab wavelet transform
                elif operation == 'python':
                    pass
                else:
                    waves, freqs = _matlab_wavelet(cwt_samples=cwt_samples)  # run matlab wavelet transform
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:  # default wavelet
            waves, freqs = _matlab_wavelet(cwt_samples=cwt_samples)  # run matlab wavelet transform

        # save cwt results as numpy array
        self.waves = np.array(waves)
        self.waves_freqs = np.array(freqs).reshape(-1)
        self.f_power = power.Power.to_freq_power(waves=self.waves)
        self.t_power = power.Power.to_time_power(waves=self.waves)
