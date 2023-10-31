import numpy as np
cimport numpy as np
from .network cimport NeuralNetwork, DenseLayer
from .ensemble cimport Ensemble


cpdef tuple[np.ndarray, tuple] encode_neural_network(
    NeuralNetwork module,
) except *:
    cdef list weights = [], decode_guide = []

    # unpack all layers
    for layer in module._layers:
        weights.append(layer._weights.reshape(-1, 1))
        weights.append(layer._biases.reshape(-1, 1))
        decode_guide.append((
            layer._weights.shape,
            layer._biases.shape,
            layer._activation,
        ))

    return np.concatenate(weights), decode_guide


cpdef NeuralNetwork decode_neural_network(
    np.ndarray weights_vector, list[tuple] decode_guide
) except *:
    module = NeuralNetwork(0)

    for weights_shape, bias_shape, activation in decode_guide:
        x, y = weights_shape
        a, b = bias_shape

        # unpack weights
        weights = weights_vector[: x * y].reshape((x, y))
        weights_vector = weights_vector[x * y:]

        # unpack biases
        biases = weights_vector[: a * b].reshape((a, b))
        weights_vector = weights_vector[a * b:]

        # add layer to network
        module.add_layer(DenseLayer(y, x, activation))
        module._layers[len(module._layers) - 1]._weights = weights
        module._layers[len(module._layers) - 1]._biases = biases

    return module


cpdef Ensemble decode_ensemble(
    np.ndarray weights_vector, list[tuple] decode_guide, str loss_function='rmse',
) except *:
    ensemble = Ensemble(loss_function=loss_function)

    for i in range(weights_vector.shape[0]):
        module = decode_neural_network(weights_vector[i], decode_guide)
        ensemble.add_network(module)

    return ensemble
