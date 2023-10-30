import os
import numpy as np

import core.antslogger as log
import core.antstimeseries as timeseries
import preprocessing.filters as filters
import postprocessing.scale as scale
import matplotlib.pyplot as plt


class Plots(timeseries.TimeSeries):
    def __init__(self):
        super(Plots, self).__init__()

    def power_spectrum(self, **kwargs):
        figure_path = os.path.join(os.path.dirname(os.getcwd()), 'figures')
        os.makedirs(figure_path, exist_ok=True)  # make 'figures' directory

        fig, ax = plt.subplots()

        # plot power sepctrum with sem
        if 'mean' and 'sem' and 'freqs' in kwargs:
            freqs = kwargs.get('freqs')
            mean = kwargs.get('mean')
            sem = kwargs.get('sem')
            if isinstance(freqs, np.ndarray) and isinstance(mean, np.ndarray) and isinstance(sem, np.ndarray):
                ax.fill_between(freqs, mean - sem, mean + sem, alpha=0.5)
                ax.plot(freqs, mean)
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            ax.plot(self.waves_freqs, self.f_power)  # Default plot
            plt.autoscale(enable=True, axis='x', tight=True)
            plt.autoscale(enable=True, axis='y', tight=True)

        # X-axis (frequency) scope
        if 'xscope' in kwargs:
            frequency_scope = kwargs.get('xscope')
            if isinstance(frequency_scope, list) or isinstance(frequency_scope, np.ndarray):
                plt.xlim(frequency_scope[0], frequency_scope[-1])  # set xlim
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')

        # Y-axis (Power) scope
        if 'yscope' in kwargs:
            power_scope = kwargs.get('yscope')
            if isinstance(power_scope, list) or isinstance(power_scope, np.ndarray):
                plt.ylim(power_scope[0], power_scope[-1])  # set ylim
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')

        # Y-axis (Power) scale
        if 'yscale' in kwargs:
            y_scale_type = kwargs.get('yscale')
            if isinstance(y_scale_type, str):
                plt.yscale(y_scale_type)  # set y scale
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')

        # save spectrum
        if 'directory' in kwargs:
            directory = kwargs.get('directory')
            if isinstance(directory, str):
                fig.savefig(os.path.join(directory, 'power_spectrum.png'))
            else:
                log.logger_handler.throw_warning(warn_code='0004', warn_msg='Default Path Selected')
                fig.savefig(os.path.join(figure_path, 'power_spectrum.png'))
        else:
            fig.savefig(os.path.join(figure_path, 'power_spectrum.png'))
        return fig, os.path.join(figure_path, 'power_spectrum.png')

    def plot_eeg(self, **kwargs):
        # Variables
        samples = np.ndarray
        time_s = np.ndarray

        figure_path = os.path.join(os.path.dirname(os.getcwd()), 'figures')
        os.makedirs(figure_path, exist_ok=True)  # make 'figures' directory

        fig, ax = plt.subplots()

        # set plot samples
        if 'target_band' in kwargs:
            target_band = kwargs.get('target_band')
            if isinstance(target_band, list) or isinstance(target_band, np.ndarray):
                samples = filters.Filters.butter(samples=self.samples, sample_frequency=self.sample_frequency,
                                                 target_band=target_band)  # filtered samples
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            samples = self.samples  # default samples

        # plot eeg
        if 'duration' in kwargs:
            duration = kwargs.get('duration')
            if isinstance(duration, list) or isinstance(duration, np.ndarray):
                time_s = scale.Scale.ts_to_sec(self.timestamps, self.sample_frequency)  # convert ts to second
                _start = int(duration[0] * self.sample_frequency)
                _end = int(duration[-1] * self.sample_frequency)
                ax.plot(time_s[_start:_end], samples[_start:_end])
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            time_s = scale.Scale.ts_to_sec(self.timestamps, self.sample_frequency)  # convert ts to second
            _start = 0
            _end = len(time_s)
            ax.plot(time_s[_start:_end], samples[_start:_end])  # default plot
            log.logger_handler.throw_warning(warn_code='0003', warn_msg='Value Warning: Few samples can be lost.')

        # save spectrum
        if 'directory' in kwargs:
            directory = kwargs.get('directory')
            if isinstance(directory, str):
                fig.savefig(os.path.join(directory, 'eeg.png'))
            else:
                log.logger_handler.throw_warning(warn_code='0004', warn_msg='Default Path Selected')
                fig.savefig(os.path.join(figure_path, 'eeg.png'))
        else:
            fig.savefig(os.path.join(figure_path, 'eeg.png'))
        return fig, os.path.join(figure_path, 'eeg.png')
