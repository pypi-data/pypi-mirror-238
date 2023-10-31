import numpy as np
cimport numpy as np


cdef class BaseFunction:
    cpdef double evaluate(self, np.ndarray individual) except *
