import numpy as np
cimport numpy as np
from .base_function cimport BaseFunction


cdef class RastriginFunction(BaseFunction):
    cdef int _dimension
    cpdef double evaluate(self, np.ndarray individual) noexcept
