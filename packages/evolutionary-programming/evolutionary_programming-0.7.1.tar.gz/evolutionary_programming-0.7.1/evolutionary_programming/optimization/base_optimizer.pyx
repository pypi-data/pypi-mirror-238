import numpy as np
cimport numpy as np
from evolutionary_programming.objective_function.base_function cimport BaseFunction


cdef class PopulationBasedOptimizer:
    def __init__(
        self,
        int n_individuals,
        int n_dims,
        list min_bounds,
        list max_bounds,
    ) -> None:
        self._n_individuals = n_individuals
        self._n_dims = n_dims
        self._min_bounds = min_bounds
        self._max_bounds = max_bounds
        self.history = []

    cdef void _init_individuals(self) except *:
        raise NotImplementedError

    cpdef np.ndarray get_population(self) except *:
        raise NotImplementedError

    cdef void _optimize_step (self, BaseFunction function) except *:
        raise NotImplementedError

    cpdef void optimize(self, int iterations, BaseFunction function) except *:
        for i in range(iterations):
            self._optimize_step(function)
            self.history.append(self.best_fitness)
            print(
                f' [{i + 1}/{iterations}] '
                f'current min value: {self.best_fitness:.6f}', end='\r'
            )
        print()
