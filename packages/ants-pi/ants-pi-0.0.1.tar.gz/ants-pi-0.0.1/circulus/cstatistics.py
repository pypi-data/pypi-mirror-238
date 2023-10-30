import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

import core.antslogger as log
import core.antstimeseries as timeseries


class Cstatistics(timeseries.TimeSeries):

    def __init__(self):
        super(Cstatistics, self).__init__()

    def get_phase(self, **kwargs):
        if 'duration' in kwargs:  # set sample duration
            duration_s = kwargs.get('duration')
            if isinstance(duration_s, list):
                duration_ts = [int((dur * self.sample_frequency) - 1) if dur > 0 else 0 for dur in duration_s]
                samples = self.samples[duration_ts[0]:duration_ts[-1]].tolist()  # slicing samples within given duration
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                samples = self.samples.tolist()
        else:
            samples = self.samples.tolist()

        # predict phase
        spectrum = sp.signal.hilbert(samples)  # hilbert transform
        phase_rad = np.angle(spectrum)  # convert phase to angle in radians

        return phase_rad

    @classmethod
    def phase(cls, samples, sample_frequency, **kwargs):
        if 'duration' in kwargs:  # set sample duration
            duration_s = kwargs.get('duration')
            if isinstance(duration_s, list):
                duration_ts = [int((dur * sample_frequency) - 1) if dur > 0 else 0 for dur in duration_s]
                samples = samples[duration_ts[0]:duration_ts[-1]].tolist()  # slicing samples within given duration
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                samples = samples.tolist()
        else:
            samples = samples.tolist()

        # predict phase
        spectrum = sp.signal.hilbert(samples)  # hilbert transform
        phase_rad = np.angle(spectrum)  # convert phase to angle in radians

        return phase_rad

    @classmethod
    def mean_resultant_vector(cls, alpha, **kwargs):
        # variables
        dim = 0  # 1-D <'dim' is fixed 1-D now. However, it will revise later>
        if 'weights' in kwargs:  # when weights are given
            weights = kwargs.get('weights')
            if np.size(weights, 1) != np.size(alpha, 1) or np.size(weights, 0) != np.size(alpha, 0):
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            weights = np.ones(np.shape(alpha))  # default weights

        # compute weighted sum of cos and sin of angles
        resultant_vector = sum(np.multiply(weights, np.exp(1j * alpha)), dim)

        # obtain angles
        resultant_vector = np.divide(np.abs(resultant_vector), sum(weights, dim))
        return resultant_vector

    @classmethod
    def kappa(cls, alpha, **kwargs):
        # variables
        alpha = np.array(alpha).reshape(-1, 1)  # to column
        N = np.shape(alpha)[-1]
        if 'weights' in kwargs:  # when weights are given
            weights = kwargs.get('weights')
            if np.size(weights, 1) > np.size(weights, 0):
                weights.reshape(-1, 1)
        else:
            weights = np.ones(np.shape(alpha))  # default weights

        if N > 1:
            R = Cstatistics.mean_resultant_vector(alpha=alpha, weights=weights)
        else:
            R = alpha

        if R < 0.53:
            kappa = 2 * R + R ** 3 + 5 * R ** 5 / 6
        elif 0.53 <= R < 0.85:
            kappa = -0.4 + 1.39 * R + 0.43 / (1 - R)
        else:
            kappa = 1 / (R ** 3 - 4 * R ** 2 + 3 * R)

        if 1 < N < 15:
            if kappa < 2:
                kappa = max(kappa - 2 * (N * kappa) ** -1, 0)
            else:
                kappa = (N - 1) ** 3 * kappa / (N ** 3 + N)
        return kappa.item()

    @classmethod
    def mean_confidence(cls, alpha, **kwargs):
        # variables
        dim = 0  # 1-D <'dim' is fixed 1-D now. However, it will revise later>
        xi = 0.05
        if 'weights' in kwargs:  # when weights are given
            weights = kwargs.get('weights')
            if np.size(weights, 1) != np.size(alpha, 1) or np.size(weights, 0) != np.size(alpha, 0):
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            weights = np.ones(np.shape(alpha))  # default weights

        # compute ingredients for confidence limits
        r = Cstatistics.mean_resultant_vector(alpha=alpha, weights=weights)
        n = sum(weights, dim)
        R = np.multiply(n, r)
        c2 = sp.stats.chi2.ppf((1 - xi), df=1)

        # check for resultant vector length and select appropriate formula
        t = np.zeros(np.shape(r))
        shape_t = np.shape(t)  # original shape of t

        r_reshape = np.array(r).reshape(-1)  # reshape to 1-D to access element wise
        t_reshape = np.array(t).reshape(-1)  # reshape to 1-D to access element wise
        R_reshape = np.array(R).reshape(-1)  # reshape to 1-D to access element wise
        n_reshape = np.array(n).reshape(-1)  # reshape to 1-D to access element wise
        for i, _ in enumerate(np.array(r).reshape(-1)):  # reshape to 1-D to access element wise
            if r_reshape[i] < 0.9 and i > np.sqrt(c2 / 2 / n_reshape[i]):
                t_reshape[i] = np.sqrt(
                    (2 * n_reshape[i] * (2 * R_reshape[i] ** 2 - n_reshape[i] * c2)) / (4 * n_reshape[i] - c2))
            elif r_reshape[i] >= 0.9:
                t_reshape[i] = np.sqrt(
                    n_reshape[i] ** 2 - (n_reshape[i] ** 2 - R_reshape[i] ** 2) * np.exp(c2 / n_reshape[i]))
            else:
                t_reshape[i] = np.nan
                log.logger_handler.throw_warning(warn_code='0003',
                                                 warn_msg='Value Warning: Requirements for confidence levels not met.')

        # reshape to original shape
        t.reshape(shape_t)

        # apply final transform
        t = np.arccos(np.divide(t, R))
        return t

    @classmethod
    def mean_direction(cls, alpha, **kwargs):
        # variables
        dim = 0  # 1-D <'dim' is fixed 1-D now. However, it will revise later>
        if 'weights' in kwargs:
            weights = kwargs.get('weights')
            if np.size(weights, 1) != np.size(alpha, 1) or np.size(weights, 0) != np.size(alpha, 0):
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
        else:
            weights = np.ones(np.shape(alpha))  # default weights

        # compute weighted sum of cos and sin of angles
        resultant_vector = sum(np.multiply(weights, np.exp(1j * alpha)), dim)

        # obtain mean by
        mu = np.angle(resultant_vector)  # mean direction

        # confidence limits if desired
        if len(kwargs) >= 1:
            t = Cstatistics.mean_confidence(alpha=alpha, weights=weights)
            ul = mu + t  # upper 95% confidence limit
            ll = mu - t  # lower 95% confidence limit
        return dict(mean_direction=mu.item(), upper_limit=ul.item(), lower_limit=ll.item())

    @classmethod
    def von_mises_parameter(cls, alpha, **kwargs):
        # variables
        alpha = np.array(alpha).reshape(-1, 1)  # to column
        dim = 0  # 1-D <'dim' is fixed 1-D now. However, it will revise later>
        if 'weights' in kwargs:  # when weights are given
            weights = kwargs.get('weights')
        else:
            weights = np.ones(np.shape(alpha))  # default weights

        resultant_vector = Cstatistics.mean_resultant_vector(alpha=alpha, weights=weights)
        kappa = Cstatistics.kappa(alpha=resultant_vector)
        thetahat = Cstatistics.mean_direction(alpha=alpha, weights=weights)
        return thetahat, kappa

    def get_preferred_phase(self, spike_peak_ts_idx, **kwargs):
        phase_rad = Cstatistics.phase(self.samples, self.sample_frequency)  # predict phase
        spike_phase = [phase_rad[ts_idx] for ts_idx in enumerate(spike_peak_ts_idx)]  # get spike phase
        (preferred_phase, kappa) = Cstatistics.von_mises_parameter(alpha=spike_phase)  # calculate preferred phase
        return preferred_phase, kappa

    @classmethod
    def preferred_phase(cls, samples, sample_frequency, spike_peak_ts_idx, **kwargs):
        phase_rad = Cstatistics.phase(samples, sample_frequency)  # predict phase
        spike_phase = [phase_rad[ts_idx] for ts_idx in spike_peak_ts_idx]  # get spike phase
        (preferred_phase, kappa) = Cstatistics.von_mises_parameter(alpha=spike_phase)  # calculate preferred phase
        return preferred_phase, kappa
