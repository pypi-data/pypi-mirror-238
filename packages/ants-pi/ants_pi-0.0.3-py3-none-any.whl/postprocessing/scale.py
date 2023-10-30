import numpy as np
import core.antstimeseries as timeseries


class Scale(timeseries.TimeSeries):
    def __init__(self):
        super(Scale, self).__init__()

    @classmethod
    def ts_to_sec(cls, timestamps, sample_frequency):
        # variables
        _start = 0
        _duration_s = int((timestamps[-1] - timestamps[0]) / 1000000)

        time_s = np.linspace(start=_start, stop=_duration_s, num=sample_frequency * _duration_s)
        return time_s

    @classmethod
    def sec_to_ts_idx(cls, time_s, sample_frequency):
        # variables
        _start = 0

        timestamp_idx = [int(_start + (time_s[i] * sample_frequency)) for i, _ in enumerate(time_s)]
        return timestamp_idx
