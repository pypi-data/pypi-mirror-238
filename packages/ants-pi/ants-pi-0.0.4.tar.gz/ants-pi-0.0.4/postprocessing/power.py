import core.antslogger as log
import numpy as np
import scipy as sp
import core.antstimeseries as timeseries


class Power(timeseries.TimeSeries):
    def __init__(self):
        super(Power, self).__init__()

    @classmethod
    def to_freq_power(cls, waves):
        f_power = np.mean((np.abs(waves)) ** 2, 1)
        return f_power

    @classmethod
    def to_time_power(cls, waves):
        t_power = np.mean((np.abs(waves)) ** 2, 0)
        return t_power

    @classmethod
    def stack_power(cls, ants):
        f_power_len = [len(ants[i].f_power) for i, _ in enumerate(ants)]
        max_len = max(f_power_len)
        freqs = ants[np.argmax(f_power_len)].waves_freqs

        # stack f_power
        stack = np.array([ants[i].f_power if f_power_len[i] == max_len else
                          np.append(ants[i].f_power, np.repeat(np.nan, max_len - f_power_len[i]))
                          for i, ant in enumerate(ants)])
        return dict(frequency=freqs, stack=stack)

    @classmethod
    def sem(cls, **kwargs):
        if 'stack' in kwargs:
            stack_dict = kwargs.get('stack')
            freqs, stack = stack_dict['frequency'], stack_dict['stack']
        elif 'batch' in kwargs:
            batch = kwargs.get('batch')
            if isinstance(batch, list) or isinstance(batch, np.ndarray):
                stack_dict = Power.stack_power(ants=batch)
                freqs, stack = stack_dict['frequency'], stack_dict['stack']
            else:
                log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
                return None
        else:
            log.logger_handler.throw_error(err_code='0003', err_msg='Value Error')
            return None

        mean = np.mean(stack, 0)
        se_m = sp.stats.sem(a=stack, nan_policy='omit')
        return freqs, mean, se_m
