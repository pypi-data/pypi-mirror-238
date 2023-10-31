import numpy as np
cimport numpy as np
from .base_optimizer cimport PopulationBasedOptimizer

from evolutionary_programming.objective_function.base_function cimport BaseFunction


cdef extern from "float.h":
    const double DBL_MAX


cdef class ParticleSwarm(PopulationBasedOptimizer):
    # does not access via python code
    cdef int _max_stagnation_interval
    cdef double _scaling_factor
    cdef double _cj
    cdef double _cognitive
    cdef double _social
    cdef double _inertia
    cdef list _individuals

    cdef void _fitness_compute(self, int i, BaseFunction function) except *
    cdef void _optimize_step(self, BaseFunction function) except *
    cpdef np.ndarray get_population(self) except *
    cpdef void optimize(self, int iterations, BaseFunction function) except *
