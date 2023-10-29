import numpy as np
cimport numpy as np
from .base_function cimport BaseFunction


cdef class RootMeanSquaredErrorForNN(BaseFunction):
    cdef np.ndarray _x_data
    cdef np.ndarray _y_data
    cdef list[tuple] _decode_guide
    cdef double _l2_regularization
    cdef np.ndarray _mask

    cpdef double evaluate(self, np.ndarray individual) except *


cdef class R2ScoreForNN(BaseFunction):
    cdef np.ndarray _x_data
    cdef np.ndarray _y_data
    cdef list[tuple] _decode_guide
    cdef double _l2_regularization
    cdef np.ndarray _mask

    cpdef double evaluate(self, np.ndarray individual) except *
