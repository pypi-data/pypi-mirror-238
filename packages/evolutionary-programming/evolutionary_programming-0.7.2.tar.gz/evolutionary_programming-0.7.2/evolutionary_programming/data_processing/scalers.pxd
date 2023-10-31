import numpy as np
cimport numpy as np


cdef class BaseScaler:
    cdef readonly bint fitted

    cpdef BaseScaler fit(self, np.ndarray data) except *
    cpdef np.ndarray transform(self, np.ndarray data) except *
    cpdef np.ndarray fit_transform(self, np.ndarray data) except *
    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *


cdef class StandardScaler(BaseScaler):
    cdef readonly double _mean
    cdef readonly double _std

    cpdef BaseScaler fit(self, np.ndarray data) except *
    cpdef np.ndarray transform(self, np.ndarray data) except *
    cpdef np.ndarray fit_transform(self, np.ndarray data) except *
    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *


cdef class MinMaxScaler(BaseScaler):
    cdef readonly double _min
    cdef readonly double _max

    cpdef BaseScaler fit(self, np.ndarray data) except *
    cpdef np.ndarray transform(self, np.ndarray data) except *
    cpdef np.ndarray fit_transform(self, np.ndarray data) except *
    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *
