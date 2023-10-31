import numpy as np
cimport numpy as np
from numpy cimport ndarray


cdef dict[str, RegularizationFunction] REGULARIZATION_FUNCTIONS = {
    'l1': l1_regularization,
    'l2': l2_regularization,
}


cdef dict[str, LearningRateDecayFunction] LR_DECAY_FUNCTIONS = {
    'none': learning_rate_no_decay,
    'exponential': learning_rate_exponential_decay,
    'staircase': learning_rate_staircase_decay,
    'time_based': learning_rate_time_based_decay,
}


cdef ndarray l1_regularization(ndarray weights, bint derivative) except *:
    if derivative:
        return np.array([np.where(w >= 0, 1, -1) for w in weights])
    return np.sum([np.sum(np.abs(w)) for w in weights], keepdims=True)


cdef ndarray l2_regularization(ndarray weights, bint derivative) except *:
    if derivative:
        return weights
    return 0.5 * np.sum(weights**2, keepdims=True)


cdef double learning_rate_no_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *:
    return learning_rate


cdef double learning_rate_time_based_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *:
    return learning_rate / (1 + decay_rate * epoch)


cdef double learning_rate_exponential_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *:
    return learning_rate * decay_rate**epoch


cdef double learning_rate_staircase_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *:
    return learning_rate * decay_rate ** (epoch // decay_steps)
