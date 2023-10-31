from numpy cimport ndarray


ctypedef ndarray (*RegularizationFunction)(ndarray, bint) except *


ctypedef ndarray (*LearningRateDecayFunction)(double, int, double, int) except *


cdef dict[str, LearningRateDecayFunction] LR_DECAY_FUNCTIONS


cdef dict[str, LearningRateDecayFunction] REGULARIZATION_FUNCTIONS


cdef ndarray l1_regularization(ndarray weights, bint derivative) except *


cdef ndarray l2_regularization(ndarray weights, bint derivative) except *


cdef double learning_rate_no_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *


cdef double learning_rate_time_based_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *


cdef double learning_rate_exponential_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *


cdef double learning_rate_staircase_decay(double learning_rate, int epoch, double decay_rate, int decay_steps) except *
