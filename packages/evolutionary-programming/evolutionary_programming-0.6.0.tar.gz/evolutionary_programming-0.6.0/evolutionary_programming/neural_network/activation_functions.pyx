import numpy as np
cimport numpy as np
from numpy cimport ndarray


cdef dict[str, ActivationFunction] ACTIVATION_FUNCTIONS = {
    'softmax': softmax,
    'sigmoid': sigmoid,
    'tanh': tanh,
    'linear': linear,
    'relu': relu,
}


cdef ndarray sigmoid(ndarray x, bint derivative) except *:
    sigma = 1 / (1.0 + np.exp(-x))
    return sigma * (1 - sigma) if derivative else sigma


cdef ndarray tanh(ndarray x, bint derivative) except *:
    if derivative:
        return 1 - tanh(x, derivative=False)**2
    return (np.exp(x) - np.exp(-x)) / ((np.exp(x) + np.exp(-x)))


cdef ndarray linear(ndarray x, bint derivative) except *:
    return np.ones_like(x) if derivative else x


cdef ndarray relu(ndarray x, bint derivative) except *:
    if derivative:
        return np.where(x <= 0, 0, 1)
    return np.maximum(0, x)


cdef ndarray softmax(ndarray x, bint derivative) except *:
    e_x = np.exp(x - np.max(x))
    sum_e_x = e_x.sum(axis=1, keepdims=True)
    result = e_x / sum_e_x

    if derivative:
        result *= 1 - result

    return result
