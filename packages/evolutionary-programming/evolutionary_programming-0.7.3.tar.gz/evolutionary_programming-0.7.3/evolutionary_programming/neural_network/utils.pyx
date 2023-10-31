import numpy as np
cimport numpy as np
from numpy cimport ndarray


cdef dict[str, WeightInitializer] WEIGHT_INITIALIZERS = {
    'ones': ones_initializer,
    'zeros': zeros_initializer,
    'random_uniform': random_uniform_initializer,
    'glorot_uniform': glorot_uniform_initializer,
    'glorot_normal': glorot_normal_initializer,
}


def batch_sequential(np.ndarray x, np.ndarray y, int batch_size = -1):
    cdef int batch_length = x.shape[0] if batch_size == -1 else batch_size
    cdef int n_batches = int(np.ceil(x.shape[0] / batch_length))
    cdef int offset = 0
    # iterate over data
    for i in range(n_batches):
        offset = batch_length * i
        x_batch = x[offset: offset + batch_length]
        y_batch = y[offset: offset + batch_length]
        yield x_batch, y_batch


cdef ndarray ones_initializer(int rows, int cols) except *:
    return np.ones((rows, cols))


cdef ndarray zeros_initializer(int rows, int cols) except *:
    return np.zeros((rows, cols))


cdef ndarray random_uniform_initializer(int rows, int cols) except *:
    return np.random.randn(rows, cols)


cdef ndarray glorot_uniform_initializer(int rows, int cols) except *:
    limit = np.sqrt(6.0 / (rows + cols))
    return 2 * limit * np.random.randn(rows, cols) - limit


cdef ndarray glorot_normal_initializer(int rows, int cols) except *:
    std_dev = np.sqrt(2.0 / (rows + cols))
    return std_dev * np.random.randn(rows, cols)
