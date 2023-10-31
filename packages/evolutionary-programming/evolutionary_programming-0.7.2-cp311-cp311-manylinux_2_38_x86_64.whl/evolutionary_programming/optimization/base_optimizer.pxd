import numpy as np
cimport numpy as np
from evolutionary_programming.objective_function.base_function cimport BaseFunction


cdef class PopulationBasedOptimizer:
    cdef readonly np.ndarray best_individual
    cdef readonly float best_fitness
    cdef readonly list history

    # does not access via python code
    cdef int _n_individuals
    cdef int _n_dims
    cdef list _min_bounds
    cdef list _max_bounds
    cdef bint _bounded

    cpdef np.ndarray get_population(self) except *
    cdef void _init_individuals(self) except *
    cdef void _optimize_step(self, BaseFunction function) except *
    cpdef void optimize(self, int iterations, BaseFunction function) except *
