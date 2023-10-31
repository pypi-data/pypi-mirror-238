import numpy as np
cimport numpy as np
from .base_optimizer cimport PopulationBasedOptimizer

from evolutionary_programming.objective_function.base_function cimport BaseFunction


cdef extern from "float.h":
    const double DBL_MAX


cdef class GeneticAlgorithm(PopulationBasedOptimizer):
    # does not access via python code
    cdef double _mutation_probability
    cdef tuple _children_shape
    cdef np.ndarray _individuals
    cdef np.ndarray _old_individuals
    cdef np.ndarray _individuals_fitness
    cdef int _elitist_individuals
    cdef double _crossover_probability
    cdef list _worst_indices
    cdef list _best_indices
    cdef list _old_best_indices

    cdef void _fitness_compute(self, BaseFunction function) except  *
    cdef np.ndarray _select_fathers(self) except *
    cdef np.ndarray _crossover(self, np.ndarray fathers_a, np.ndarray fathers_b) except *
    cdef np.ndarray _mutation(self, np.ndarray children) except *
    cdef void _optimize_step(self, BaseFunction function) except *
    cpdef void optimize(self, int iterations, BaseFunction function) except *
    cpdef np.ndarray get_population(self) except *
