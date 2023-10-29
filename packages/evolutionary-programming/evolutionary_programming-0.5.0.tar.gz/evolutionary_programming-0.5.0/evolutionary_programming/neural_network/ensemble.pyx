import pickle
import numpy as np
cimport numpy as np
from copy import deepcopy
from .network cimport NeuralNetwork
from .loss_functions cimport LOSS_FUNCTIONS


cdef class Ensemble:
    def __cinit__(
        self,
        str loss_function = 'mse',
        networks=None,
    ):
        self._loss_function_fn = LOSS_FUNCTIONS.get(loss_function)
        self._networks = []
        if networks is not None:
            self.add_network(networks)

    cpdef void add_network(self, network) except *:
        if isinstance(network, list):
            self._networks.extend(network)
        elif isinstance(network, NeuralNetwork):
            self._networks.append(network)
        else:
            raise TypeError('Only support NeuralNetwork or list[NeuralNetwork] types')

    cpdef double evaluate(self, np.ndarray x, np.ndarray y, str loss_name=None) except *:
        loss_fn = self._loss_function_fn if loss_name is None else LOSS_FUNCTIONS.get(loss_name)
        y_hat = self.predict(x)
        return loss_fn(y, y_hat, derivative=False).item()

    cpdef np.ndarray predict(self, np.ndarray x) except *:
        return np.mean(np.array([
            network.predict(x) for network in self._networks]), axis=0)

    cpdef void save(self, str file_path) except *:
        pickle.dump(self, open(file_path, 'wb'), pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(file_path: str) -> Ensemble:
        with open(file_path, 'rb') as file:
            return pickle.load(file)

    def __reduce__(self) -> tuple[function[tuple, Ensemble], tuple]:
        return (_rebuild_ensemble, (
                self._loss_function, deepcopy(self._networks)
            )
        )


cpdef Ensemble _rebuild_ensemble(str loss_function, list[NeuralNetwork] networks) except *:
    ensemble = Ensemble(loss_function)
    ensemble._networks = networks
    return ensemble
