import numpy as np
import core.antstimeseries as timeseries


class Normalization(timeseries.TimeSeries):
    def __init__(self):
        super(Normalization, self).__init__()

    def normalization(self, method):
        if method == 'rms':
            root_mean_square = np.sqrt(np.mean(self.samples ** 2))
            self.samples /= root_mean_square
        elif method == 'zscore':
            pass
