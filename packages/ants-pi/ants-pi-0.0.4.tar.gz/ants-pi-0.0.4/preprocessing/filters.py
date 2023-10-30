import scipy as sp
import core.antstimeseries as timeseries


class Filters(timeseries.TimeSeries):
    def __init__(self):
        super(Filters, self).__init__()

    def bandpass_butter(self, target_band):
        nyquist = self.sample_frequency * 0.5
        sos = sp.signal.butter(N=6, Wn=[f / nyquist for f in target_band], btype='bandpass',
                               analog=False, output='sos')
        self.bandpass_samples = sp.signal.sosfiltfilt(sos=sos, x=self.samples)

    @classmethod
    def butter(cls, samples, sample_frequency, target_band):
        nyquist = sample_frequency * 0.5
        sos = sp.signal.butter(N=6, Wn=[f / nyquist for f in target_band], btype='bandpass',
                               analog=False, output='sos')
        bandpass_samples = sp.signal.sosfiltfilt(sos=sos, x=samples)
        return bandpass_samples
