import numpy as np
cimport numpy as np
from .base_function cimport BaseFunction
from evolutionary_programming.neural_network.coding cimport decode_neural_network


cdef class RootMeanSquaredErrorForNN(BaseFunction):
    def __init__(
        self,
        np.ndarray x_data,
        np.ndarray y_data,
        list[tuple] decode_guide,
        double l2_regularization = 0.0,
    ):
        super().__init__()
        self._x_data = x_data
        self._y_data = y_data
        self._decode_guide = decode_guide
        self._l2_regularization = l2_regularization

        # build mask to apply regularization only to weights
        mask = []

        for weight, bias, _ in decode_guide:
            weights = weight[0] * weight[1]
            biases = bias[0] * bias[1]
            mask.extend(
                [True for _ in range(weights)] +
                [False for _ in range(biases)]
            )

        self._mask = np.array(mask, dtype=bool)

    cpdef double evaluate(self, np.ndarray individual) except *:
        # decode network
        nn = decode_neural_network(individual, self._decode_guide)

        with np.errstate(all='raise'):
            try:
                y_hat = nn.predict(self._x_data)
            except FloatingPointError:
                return float('inf')

        # compute error
        error = np.sqrt(np.mean((y_hat - self._y_data) ** 2))
        if self._l2_regularization > 0:
            error += self._l2_regularization * np.sum(individual[self._mask]**2)

        return error


cdef class R2ScoreForNN(BaseFunction):
    def __init__(
        self,
        np.ndarray x_data,
        np.ndarray y_data,
        list[tuple] decode_guide,
        double l2_regularization = 0.0,
    ):
        super().__init__()
        self._x_data = x_data
        self._y_data = y_data
        self._decode_guide = decode_guide
        self._l2_regularization = l2_regularization

        # build mask to apply regularization only to weights
        mask = []

        for weight, bias, _ in decode_guide:
            weights = weight[0] * weight[1]
            biases = bias[0] * bias[1]
            mask.extend(
                [True for _ in range(weights)] +
                [False for _ in range(biases)]
            )

        self._mask = np.array(mask, dtype=bool)

    cpdef double evaluate(self, np.ndarray individual) except *:
        # decode network
        nn = decode_neural_network(individual, self._decode_guide)

        with np.errstate(all='raise'):
            try:
                y_hat = nn.predict(self._x_data)
            except FloatingPointError:
                return float('inf')

        # compute error
        ssr = np.sum((self._y_data - y_hat)**2)
        sst = np.sum((self._y_data - np.mean(self._y_data))**2)
        error = 1 - (ssr / sst)
        if self._l2_regularization > 0:
            error += self._l2_regularization * np.sum(individual[self._mask]**2)

        return error
