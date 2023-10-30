import os
import numpy as np
import mat73 as readmat
import matlab
import matlab.engine as me
import core.antslogger as log
import core.antsplatform as platform
import core.antstimeseries as timeseries
import extractor.nlx_in_matlab_win as nlxW


class Caller(timeseries.TimeSeries):
    def __init__(self):
        super(Caller, self).__init__()

    def call_neuralynx(self, path):
        os = platform.check_os()

        if os == 'win':  # Windows
            # # variables
            # field_selection_flags = [1, 0, 1, 0, 1]
            # header_extraction_flag = 1
            # extraction_mode = 1
            # extraction_mode_vector = 1
            #
            # mat_engine = me.start_matlab()  # start matlab engine
            # nlx_path = str(nlxW.__path__.__dict__['_path'][0])  # get nlx_in_matlab module folder path
            # mat_engine.addpath(nlx_path)  # cd nlx_in_matlab module folder
            # try:
            #     (self.timestamps, self.sample_frequency,
            #      self.samples, self.header) = mat_engine.Nlx2MatCSC(path,
            #                                                         field_selection_flags,
            #                                                         header_extraction_flag,
            #                                                         extraction_mode,
            #                                                         extraction_mode_vector)
            # except:
            #     log.logger_handler.throw_error(err_code='0002', err_msg='No Files Error')

            ### bypass window matlab engine error; need refactoring ###
            try:
                mat = readmat.loadmat(path)  # load mat7.3 file, extracted by 'extract_to_ants.m"
                self.path = path
                self.header = list(mat['header'])
                self.sample_frequency = int(mat['sample_frequency'])
                self.samples = mat['samples']
                self.timestamps = mat['timestamps']
            except:
                log.logger_handler.throw_error(err_code='0002', err_msg='No Files Error')
        elif os == 'mac' or os == 'linux':  # Mac or linux
            try:
                mat = readmat.loadmat(path)  # load mat7.3 file, extracted by 'extract_to_ants.m"
                self.path = path
                self.header = list(mat['header'])
                self.sample_frequency = int(mat['sample_frequency'])
                self.samples = mat['samples']
                self.timestamps = mat['timestamps']
            except:
                log.logger_handler.throw_error(err_code='0002', err_msg='No Files Error')
        elif os == 'linux':  # Linux
            log.logger_handler.throw_error(err_code='0001', err_msg='OS Error')

    def call_nlx_events(self, path):
        os = platform.check_os()

        if os == 'win':
            pass
        elif os == 'mac':
            pass
        elif os == 'linux':
            pass
