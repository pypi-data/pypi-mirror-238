import numpy as np
cimport numpy as np
from .network cimport NeuralNetwork
from .ensemble cimport Ensemble


cpdef tuple[np.ndarray, tuple] encode_neural_network(
    NeuralNetwork module,
) except *


cpdef NeuralNetwork decode_neural_network(
    np.ndarray weights_vector, list[tuple] decode_guide
) except *


cpdef Ensemble decode_ensemble(
    np.ndarray weights_vector, list[tuple] decode_guide, str loss_function=*
) except *
