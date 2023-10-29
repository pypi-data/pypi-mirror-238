import numpy as np
cimport numpy as np
from .network cimport NeuralNetwork


cpdef tuple[np.ndarray, tuple] encode_neural_network(
    NeuralNetwork module,
) except *


cpdef NeuralNetwork decode_neural_network(
    np.ndarray weights_vector, list[tuple] decode_guide
) except *
