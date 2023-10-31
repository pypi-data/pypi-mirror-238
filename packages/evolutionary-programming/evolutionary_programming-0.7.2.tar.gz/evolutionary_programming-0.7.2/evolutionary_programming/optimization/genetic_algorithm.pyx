import numpy as np
cimport numpy as np
from .base_optimizer cimport PopulationBasedOptimizer
from evolutionary_programming.objective_function.base_function cimport BaseFunction


cdef class GeneticAlgorithm(PopulationBasedOptimizer):
    def __init__(
        self,
        int n_individuals,
        int n_dims,
        list min_bounds,
        list max_bounds,
        int elitist_individuals = 1,
        double mutation_probability = 0.01,
        double crossover_probability = 0.80,
        bint bounded = True,
    ):
        super().__init__(n_individuals, n_dims, min_bounds, max_bounds)
        self._elitist_individuals = elitist_individuals
        self._mutation_probability = mutation_probability
        self._crossover_probability = crossover_probability
        self._children_shape = (self._n_individuals, self._n_dims)
        self._bounded = bounded
        self._init_individuals()

    cdef void _init_individuals(self) except *:
        self._worst_indices = [(0, 0) for _ in range(self._elitist_individuals)]
        self._best_indices = [(0, DBL_MAX) for _ in range(self._elitist_individuals)]
        self._old_best_indices = self._best_indices.copy()

        # create individuals
        self._individuals_fitness = np.full(self._n_individuals, DBL_MAX)
        self._individuals = np.random.uniform(
            self._min_bounds, self._max_bounds, self._children_shape)
        self._old_individuals = self._individuals.copy()

        # set the best individual, temporary
        self.best_individual = self._individuals[0]
        self.best_fitness = self._individuals_fitness[0]

    cdef void _fitness_compute(self, BaseFunction function) except *:
        for i in range(self._n_individuals):
            self._individuals_fitness[i] = function.evaluate(self._individuals[i])

            # update best and worst
            for j in range(0, self._elitist_individuals):
                # best
                if self._individuals_fitness[i] < self._best_indices[j][1]:
                    self._best_indices[j] = (i, self._individuals_fitness[i])
                    # update particle best fitness
                    if j == 0:
                        self.best_fitness = self._individuals_fitness[i]
                        self.best_individual = self._individuals[i]
                    break

                # worst
                if self._individuals_fitness[i] > self._worst_indices[j][1]:
                    self._worst_indices[j] = (i, self._individuals_fitness[i])
                    break

    cdef np.ndarray _select_fathers(self) except *:
        # randomly select fathers
        fathers_0 = np.random.choice(self._n_individuals, self._n_individuals//2)
        fathers_1 = np.random.choice(self._n_individuals, self._n_individuals//2)
        return self._individuals[
            np.where(
                self._individuals_fitness[fathers_0] < self._individuals_fitness[fathers_1],
                fathers_0, fathers_1
            )
        ]

    cdef np.ndarray _crossover(self, np.ndarray fathers_a, np.ndarray fathers_b) except *:
        beta = np.random.random((self._n_individuals//2, self._n_dims))
        mask = np.random.random(self._n_individuals) < self._crossover_probability
        children = np.concatenate([fathers_a, fathers_b])
        children[mask] = np.concatenate([
            beta * fathers_a + (1 - beta) * fathers_b,
            (1 - beta) * fathers_a + beta * fathers_b,
        ])[mask]
        return children

    cdef np.ndarray _mutation(self, np.ndarray children) except *:
        mutation_mask = np.random.random(self._children_shape) <= self._mutation_probability
        mutation_values = np.random.normal(0, 1, self._children_shape)
        children = children + mutation_mask * mutation_values
        return children

    cpdef void optimize(self, int iterations, BaseFunction function) except *:
        self._fitness_compute(function)
        super(GeneticAlgorithm, self).optimize(iterations, function)

    cdef void _optimize_step(self, BaseFunction function) except *:
        # create new individuals
        children = self._crossover(self._select_fathers(), self._select_fathers())
        children = self._mutation(children)

        # force bounds
        if self._bounded:
            self._individuals = np.clip(children, self._min_bounds, self._max_bounds)
        else:
            self._individuals = children

        self._fitness_compute(function)

        # copy the best n individuals to the next gen (elitism)
        for j in range(self._elitist_individuals):
            best_ind = self._best_indices[j][0]
            worst_ind = self._worst_indices[j][0]
            self._individuals[worst_ind] = self._old_individuals[best_ind]
        self._old_individuals = self._individuals.copy()
        self._old_best_indices = self._best_indices.copy()

    cpdef np.ndarray get_population(self) except *:
        return self._individuals
