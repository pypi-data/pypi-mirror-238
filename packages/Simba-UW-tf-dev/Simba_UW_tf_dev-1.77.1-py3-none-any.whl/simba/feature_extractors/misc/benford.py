import numpy as np
from numba import njit, prange




@njit('(float32[:], float64[:], int64)')
def sliding_benford_correlation(data: np.ndarray,
                                time_windows: np.ndarray,
                                sample_rate: int) -> np.ndarray:
    """
    Calculate the sliding Benford's Law correlation coefficient for a given dataset within
    specified time windows.

    Benford's Law is a statistical phenomenon where the leading digits of many datasets follow a
    specific distribution pattern. This function calculates the correlation between the observed
    distribution of leading digits in a dataset and the ideal Benford's Law distribution.

    .. note::
       Adapted from `tsfresh <https://tsfresh.readthedocs.io/en/latest/_modules/tsfresh/feature_extraction/feature_calculators.html#benford_correlation>`_.

       The returned correlation values are calculated using Pearson's correlation coefficient.

    The correlation coefficient is calculated between the observed leading digit distribution and
    the ideal Benford's Law distribution.

    .. math::

        P(d) = \\log_{10}\\left(1 + \\frac{1}{d}\\right) \\quad \\text{for } d \\in \{1, 2, \\ldots, 9\}

    :param np.ndarray data: The input 1D array containing the time series data.
    :param np.ndarray time_windows: A 1D array containing the time windows (in seconds) for which the correlation will be calculated at different points in the dataset.
    :param int sample_rate: The sample rate, indicating how many data points are collected per second.
    :return np.ndarray: 2D array containing the correlation coefficient values for each time window. With time window lenths represented by different columns.

    :examples:
    >>> data = np.array([1, 8, 2, 10, 8, 6, 8, 1, 1, 1]).astype(np.float32)
    >>> sliding_benford_correlation(data=data, time_windows=np.array([1.0]), sample_rate=2)
    >>> [[ 0.][0.447][0.017][0.877][0.447][0.358][0.358][0.447][0.864][0.864]]
    """

    data = np.abs(data)
    benford_distribution = np.array([np.log10(1 + 1 / n) for n in range(1, 10)])
    results = np.full((data.shape[0], time_windows.shape[0]), 0.0)
    for i in prange(time_windows.shape[0]):
        window_size = int(time_windows[i] * sample_rate)
        for l, r in zip(prange(0, data.shape[0] + 1), prange(window_size, data.shape[0] + 1)):
            first_vals, digit_ratio = np.full((data.shape[0]), np.nan), np.full(9, np.nan)
            sample = data[l:r]
            for k in range(sample.shape[0]):
                first_vals[k] = (sample[k] // 10 ** (int(np.log10(sample[k])) - 1 + 1))
            for k in range(1, 10):
                digit_ratio[k - 1] = np.argwhere(first_vals == k).shape[0] / sample.shape[0]
            results[r - 1, i] = np.corrcoef(benford_distribution, digit_ratio)[0, 1]

    return results.astype(np.float32)

# data = np.array([1, 8, 2, 10, 8, 6, 8, 1, 1, 1]).astype(np.float32)
# print(np.round(sliding_benford_correlation(data=data, time_windows=np.array([1.0]), sample_rate=2), 3))














