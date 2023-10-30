import preparator.dirprep as dirprep
import extractor.caller as caller
import preprocessing.downsampling as downsampling
import preprocessing.filters as filters
import preprocessing.normalization as normalization
import timefrequency.wavelet as wavelet
import timefrequency.fft as fft
import postprocessing.power as post_power
import postprocessing.scale as scale
import painter.plots as plots
import circulus.cstatistics as cstat
import spikes.classification as classify

import os
import datetime
import pickle
import numpy as np
import core.antslogger as log


# User interface
class Ants(caller.Caller, downsampling.Downsampling, dirprep.DirPrep,
           filters.Filters, normalization.Normalization, wavelet.Wavelet, fft.FFT,
           post_power.Power, scale.Scale, plots.Plots, cstat.Cstatistics,
           classify.Classification):

    def __init__(self):
        super(Ants, self).__init__()

    @classmethod
    def make(cls, batch_size=1):
        ants = np.array([Ants() for i in np.arange(0, batch_size)])
        return ants

    @classmethod
    def save(cls, ants, path=os.path.join(os.path.expanduser('~/Documents'), 'ANTS')):
        # variables
        today = datetime.datetime.today()
        f_name = str(today.strftime('%Y_%m_%d_%H_%M')) + '_ANTS.ants'
        save_path = os.path.join(path, f_name)

        os.makedirs(path, exist_ok=True)  # make dir

        with open(save_path, "wb") as f:  # save object
            pickle.dump(len(ants), f)
            for value in ants:
                pickle.dump(value, f)
        return save_path

    @classmethod
    def load(cls, path):
        try:
            data = []
            with open(path, 'rb') as f:
                for _ in range(pickle.load(f)):
                    data.append(pickle.load(f))
            return data
        except:  # no file
            log.logger_handler.throw_error(err_code='0002', err_msg='No Files Error')
            return np.nan
