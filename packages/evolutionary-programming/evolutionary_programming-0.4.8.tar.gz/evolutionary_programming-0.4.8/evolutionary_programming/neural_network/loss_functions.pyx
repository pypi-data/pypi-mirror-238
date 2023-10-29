import numpy as np
cimport numpy as np
from numpy cimport ndarray
from .activation_functions cimport softmax


cdef dict[str, LossFunction] LOSS_FUNCTIONS = {
    'neg_log_likelihood': neg_log_likelihood,
    'softmax_neg_log_likelihood': softmax_neg_log_likelihood,
    'mae': mae,
    'mse': mse,
    'rmse': rmse,
}

cdef ndarray neg_log_likelihood(ndarray y, ndarray y_hat, bint derivative) except *:
    indices = np.nonzero(y_hat * y)
    values = y_hat[indices]

    if derivative:
        y_hat[indices] = -1.0 / values
        return y_hat

    return np.mean(-np.log(values), keepdims=True)


cdef ndarray softmax_neg_log_likelihood(ndarray y, ndarray y_hat, bint derivative) except *:
    out = softmax(y_hat, derivative=False)

    if derivative:
        return -(y - out) / y.shape[0]

    return neg_log_likelihood(y, out, derivative=False)


cdef ndarray mae(ndarray y, ndarray y_hat, bint derivative) except *:
    if derivative:
        return np.where(y_hat > y, 1, -1) / y.shape[0]
    return np.mean(np.abs(y - y_hat), keepdims=True)


cdef ndarray mse(ndarray y, ndarray y_hat, bint derivative) except *:
    if derivative:
        return (y_hat - y) / y.shape[0]
    return 0.5 * np.mean((y - y_hat) ** 2, keepdims=True)


cdef ndarray rmse(ndarray y, ndarray y_hat, bint derivative) except *:
    difference = y - y_hat
    mse_value = np.sqrt(np.mean(difference ** 2, keepdims=True))

    if derivative:
        return -difference/(y.shape[0] * mse_value)

    return mse_value
