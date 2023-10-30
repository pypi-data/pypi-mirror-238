import core.antslogger as log
import core.antstimeseries as timeseries
import postprocessing.scale as scale

import os
import numpy as np


class DirPrep(timeseries.TimeSeries):
    def __init__(self):
        super(DirPrep, self).__init__()

    @classmethod
    def get_subdirectory(cls, superior_path):
        # get directories where data is in itself
        sub_paths = [subs for subs in os.walk(superior_path) if len(subs[1]) == 0 and len(subs[-1]) != 0]
        sub_paths.sort()
        return sub_paths

    @classmethod
    def get_data_directory(cls, superior_path, **kwargs):
        # return variable
        return_dir = []

        # kwargs
        file_expander = ''  # default = all files

        if 'expander' in kwargs:
            expander = kwargs.get('expander')
            if isinstance(file_expander, str):
                file_expander = expander
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            file_expander = ''  # all files

        # get sub-directories from superior_path
        subs = cls.get_subdirectory(superior_path=superior_path)

        for sub_i, _ in enumerate(subs):  # 1st sub-dir where data files in itself
            for file_i, _ in enumerate(subs[sub_i][-1]):  # data files in the 1st sub-dir
                if subs[sub_i][-1][file_i].endswith(file_expander):  # select only specified files
                    return_dir.append(os.path.join(subs[sub_i][0],
                                                   subs[sub_i][-1][file_i]))  # append merged directory
        return np.array(return_dir)

    @classmethod
    def get_spikes(cls, superior_path, expander='txt', **kwargs):
        # kwargs
        scale_mode = kwargs.get('scale') if 'scale' in kwargs else 'sec'
        sample_frequency = kwargs.get('sample_frequency') if 'sample_frequency' in kwargs else 2000

        spikes_path = DirPrep.get_data_directory(superior_path=superior_path, expander=expander)  # get spike time

        if scale_mode == 'sec':
            spikes = [np.loadtxt(spikes_path[i]) for i, _ in enumerate(spikes_path)]
        elif scale_mode == 'idx':
            spikes = [scale.Scale.sec_to_ts_idx(time_s=np.loadtxt(spikes_path[i]), sample_frequency=sample_frequency)
                      for i, _ in enumerate(spikes_path)]
        else:  # default
            spikes = [np.loadtxt(spikes_path[i]) for i, _ in enumerate(spikes_path)]
        return spikes
