import numpy as np
cimport numpy as np
from numpy cimport ndarray


ctypedef ndarray (*ActivationFunction)(ndarray, bint) except *


cdef dict[str, ActivationFunction] ACTIVATION_FUNCTIONS


cdef ndarray sigmoid(ndarray x, bint derivative) except *


cdef ndarray tanh(ndarray x, bint derivative) except *


cdef ndarray linear(ndarray x, bint derivative) except *


cdef ndarray relu(ndarray x, bint derivative) except *


cdef ndarray softmax(ndarray x, bint derivative) except *
