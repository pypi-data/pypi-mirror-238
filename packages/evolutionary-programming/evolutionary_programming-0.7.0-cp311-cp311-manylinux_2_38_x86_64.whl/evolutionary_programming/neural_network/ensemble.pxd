import numpy as np
cimport numpy as np
from .network cimport NeuralNetwork
from typing import Any


cdef class Ensemble:
    cdef list[NeuralNetwork] _networks
    cdef str _loss_function
    cdef object _loss_function_fn
    cdef np.ndarray _weights

    cpdef void add_network(self, network) except *
    cpdef double evaluate(self, np.ndarray x, np.ndarray y, str loss_name=*) except *
    cpdef np.ndarray predict(self, np.ndarray x) except *
    cpdef void save(self, str file_path) except *
    cpdef void update_weights(self, np.ndarray x, np.ndarray y) except *


cpdef Ensemble _rebuild_ensemble(str loss_function, list[NeuralNetwork] networks) except *
