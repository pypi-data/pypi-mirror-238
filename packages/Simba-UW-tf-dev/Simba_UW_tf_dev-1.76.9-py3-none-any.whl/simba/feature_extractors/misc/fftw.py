from numba import njit, prange
import numpy as np

@njit('(float32[:], float64, int64, boolean,)')
def time_since_previous_target_value(data: np.ndarray,
                                     value: float,
                                     sample_rate: int,
                                     inverse: bool) -> np.ndarray:
    """
    Calculate the time duration (in seconds) since the previous occurrence of a specific value in a data array.

    Calculates the time duration, in seconds, between each data point and the previous occurrence
    of a specific value within the data array.

    :param np.ndarray data: The input 1D array containing the time series data.
    :param float value: The specific value to search for in the data array.
    :param int sample_rate: The sampling rate which data points were collected. It is used to calculate the time duration in seconds.
    :param bool inverse: If True, the function calculates the time since the previous value that is NOT equal to the specified 'value'. If False, it calculates the time since the previous occurrence of the specified 'value'.
    :returns np.ndarray: A 1D NumPy array containing the time duration (in seconds) since the previous occurrence of the specified 'value' for each data point.

    :example:
    >>> data = np.array([8, 8, 2, 10, 8, 6, 8, 1, 1, 1]).astype(np.float32)
    >>> time_since_previous_target_value(data=data, value=8.0, inverse=False, sample_rate=2.0)
    >>> [0. , 0. , 0.5, 1. , 0. , 0.5, 0. , 0.5, 1. , 1.5])
    >>> time_since_previous_target_value(data=data, value=8.0, inverse=True, sample_rate=2.0)
    >>> [-1. , -1. ,  0. ,  0. ,  0.5,  0. ,  0.5,  0. ,  0. ,  0. ]
    """

    results = np.full((data.shape[0]), -1.0)
    if not inverse:
        criterion_idx = np.argwhere(data == value).flatten()
    else:
        criterion_idx = np.argwhere(data != value).flatten()
    if criterion_idx.shape[0] == 0:
        return np.full((data.shape[0]), -1.0)
    for i in prange(data.shape[0]):
        if not inverse and (data[i] == value):
            results[i] = 0
        elif inverse and (data[i] != value):
            results[i] = 0
        else:
            x = criterion_idx[np.argwhere(criterion_idx < i).flatten()]
            if len(x) > 0:
                results[i] = (i - x[-1]) / sample_rate
    return results