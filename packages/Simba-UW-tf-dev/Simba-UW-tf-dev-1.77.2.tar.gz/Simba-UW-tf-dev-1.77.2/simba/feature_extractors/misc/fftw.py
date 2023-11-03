import numpy as np
from numba import njit, prange


@njit('(int32[:, :], float64[:], int64)')
def sliding_phi_coefficient(data: np.ndarray,
                            window_sizes: np.ndarray,
                            sample_rate: int) -> np.ndarray:

    """
    Calculate sliding phi coefficients for a 2x2 contingency table derived from binary data.

    Computes sliding phi coefficients for a 2x2 contingency table derived from binary data over different
    time windows. The phi coefficient is a measure of association between two binary variables, and sliding phi
    coefficients can reveal changes in association over time.

    :param np.ndarray data: A 2D NumPy array containing binary data organized in two columns. Each row represents a pair of binary values for two variables.
    :param np.ndarray window_sizes: 1D NumPy array specifying the time windows (in seconds) over which to calculate the sliding phi coefficients.
    :param int sample_rate: The sampling rate or time interval (in samples per second, e.g., fps) at which data points were collected.
    :returns np.ndarray: A 2D NumPy array containing the calculated sliding phi coefficients. Each row corresponds to the phi coefficients calculated for a specific time point, the columns correspond to time-windows.

    :example:
    >>> data = np.random.randint(0, 2, (200, 2))
    >>> sliding_phi_coefficient(data=data, window_sizes=np.array([1.0, 4.0]), sample_rate=10)
    """

    results = np.full((data.shape[0], window_sizes.shape[0]), -1.0)
    for i in prange(window_sizes.shape[0]):
        window_size = int(window_sizes[i] * sample_rate)
        for l, r in zip(range(0, data.shape[0] + 1), range(window_size, data.shape[0] + 1)):
            sample = data[l:r, :]
            cnt_0_0 = len(np.argwhere((sample[:, 0] == 0) & (sample[:, 1] == 0)).flatten())
            cnt_0_1 = len(np.argwhere((sample[:, 0] == 0) & (sample[:, 1] == 1)).flatten())
            cnt_1_0 = len(np.argwhere((sample[:, 0] == 1) & (sample[:, 1] == 0)).flatten())
            cnt_1_1 = len(np.argwhere((sample[:, 0] == 1) & (sample[:, 1] == 1)).flatten())
            BC, AD = cnt_1_1 * cnt_0_0, cnt_1_0 * cnt_0_1
            nominator = BC - AD
            denominator = np.sqrt((cnt_1_0 + cnt_1_1) * (cnt_0_0 + cnt_0_1) * (cnt_1_0 + cnt_0_0) * (cnt_1_1 * cnt_0_1))
            if nominator == 0 or denominator == 0:
                results[r - 1, i] = 0.0
            else:
                results[r - 1, i] = np.abs((BC - AD) / np.sqrt((cnt_1_0 + cnt_1_1) * (cnt_0_0 + cnt_0_1) *  (cnt_1_0 + cnt_0_0) * (cnt_1_1 * cnt_0_1)))

    return results.astype(np.float32)


data_1 = np.random.randint(0, 2, (200, 2))

# data_1 = np.random.randint(0, 1, (100,))
# data_2 = np.random.randint(0, 1, (100,))

sliding_phi_coefficient(data=data, window_sizes=np.array([1.0, 4.0]), sample_rate=10)
