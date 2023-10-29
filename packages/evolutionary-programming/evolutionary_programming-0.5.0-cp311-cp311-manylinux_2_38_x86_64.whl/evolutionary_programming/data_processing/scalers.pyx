import numpy as np
cimport numpy as np


cdef class BaseScaler:
    cpdef BaseScaler fit(self, np.ndarray data) except *:
        raise NotImplementedError

    cpdef np.ndarray transform(self, np.ndarray data) except *:
        raise NotImplementedError

    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *:
        raise NotImplementedError

    cpdef np.ndarray fit_transform(self, np.ndarray data) except *:
        self.fit(data)
        return self.transform(data)


cdef class StandardScaler(BaseScaler):
    def __init__(self) -> None:
        self._mean = 0
        self._std = 0
        self.fitted = False

    cpdef BaseScaler fit(self, np.ndarray data) except *:
        self._mean = data.mean()
        self._std = data.std()
        self.fitted = True

    cpdef np.ndarray transform(self, np.ndarray data) except *:
        return (data - self._mean) / self._std

    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *:
        return data * self._std + self._mean


cdef class MinMaxScaler(BaseScaler):
    def __init__(self) -> None:
        self._min = 0
        self._max = 0
        self.fitted = False

    cpdef BaseScaler fit(self, np.ndarray data) except *:
        self._min = data.min()
        self._max = data.max()
        self.fitted = True

    cpdef np.ndarray transform(self, np.ndarray data) except *:
        return (data - self._min) / (self._max - self._min)

    cpdef np.ndarray inverse_transform(self, np.ndarray data) except *:
        return data * (self._max - self._min) + self._min
