import numpy as np

import core.antstimeseries as timeseries


class Classification(timeseries.TimeSeries):
    def __init__(self):
        super(Classification, ).__init__()

    @classmethod
    def classify(cls, spk_s, mode='pc'):
        # variables
        duration_s = spk_s[-1] - spk_s[0]

        # firing rate
        firing_rate = len(spk_s) / duration_s

        # mad isi
        isi, mad = cls.calc_mad(spk_s=spk_s)

        # cv, cv2
        cv, cv2 = cls.calc_cv2(spk_s=spk_s)

        if mode == 'pc':  # Purkinje cell
            if firing_rate >= 40:
                if mad <= 0.008:
                    if cv2 >= 0.2:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    @classmethod
    def calc_mad(cls, spk_s):
        # calc ISI
        isi = np.diff(spk_s, axis=0)

        # calc MAD of the ISI
        mad = cls.mad(isi)
        return isi, mad

    @classmethod
    def mad(cls, data):
        return np.median(np.absolute(data - np.median(data, axis=0)), axis=0)

    @classmethod
    def calc_cv2(cls, spk_s):
        # pre-declaration
        cv2 = []

        # calc ISI
        isi = np.diff(spk_s, axis=0)

        # calc CV
        misi = np.mean(isi)
        stdisi = np.std(isi)
        cv = stdisi / misi

        # calc CV2
        for i, _ in enumerate(isi):
            if i != len(isi) - 1:  # before the last value
                cv2.append(np.abs(isi[i + 1] - isi[i]) / ((isi[i + 1] + isi[i]) / 2))

        cv2 = np.mean(cv2)
        return cv, cv2
